"""
User model signals for cache synchronization and event publishing.

This module listens to changes in the User model and ensures:
- Cache is updated or invalidated accordingly using decorators.
- A user-related event is published asynchronously via Celery.

Handled events:
- post_save: user creation or update
- post_delete: user deletion
- m2m_changed: user group assignment changes

Decorators:
- @cache_update: Updates Redis or other cache store using build_user_data.
- @cache_invalidate: Removes cached user data on delete.
"""

from django.db.models.signals import post_save, m2m_changed, post_delete
from django.dispatch import receiver
from core.constants import ConfigConstant as CoreConfigConstant, CacheConstant
from core.decorators import cache_update, cache_invalidate
from users.models import User
from users.tasks import publish_user_updated_event


def build_user_data(instance: User) -> dict:
    """
    Constructs a dictionary representation of the user, including group details.

    This is used for both caching and event publishing to ensure consistency across systems.
    """

    return {
        "id": instance.id,
        "username": instance.username,
        "email": instance.email,
        "first_name": instance.first_name,
        "last_name": instance.last_name,
        "is_active": instance.is_active,
        "group_details": [
            {"id": group.id, "name": group.name} for group in instance.groups.all()
        ],
    }


@receiver(post_save, sender=User)
@cache_update(
    source=CacheConstant.SOURCE_SIGNAL,
    data_getter=build_user_data,
    service_name=CoreConfigConstant.USER_SERVICE_NAME,
)
def user_saved(sender, instance: User, created, **kwargs):
    """
    Signal triggered after a User is saved (created or updated).

    - Updates the cache with latest user data.
    - Publishes a user update event via Celery.
    """

    user_data = build_user_data(instance)

    publish_user_updated_event({"user": user_data, "created": created})


@receiver(post_delete, sender=User)
@cache_invalidate(
    type=CacheConstant.TYPE_MODEL,
    source=CacheConstant.SOURCE_SIGNAL,
    service_name=CoreConfigConstant.USER_SERVICE_NAME,
)
def user_deleted(sender, instance: User, **kwargs):
    """
    Signal triggered after a User is deleted.

    - Invalidates the user cache.
    - Publishes a user deletion event via Celery.
    """

    user_data = build_user_data(instance)

    publish_user_updated_event({"user": user_data, "deleted": True})


@receiver(m2m_changed, sender=User.groups.through)
@cache_update(
    source=CacheConstant.SOURCE_SIGNAL,
    data_getter=build_user_data,
    service_name=CoreConfigConstant.USER_SERVICE_NAME,
)
def user_groups_changed(sender, instance: User, action, **kwargs):
    """
    Signal triggered when a User's groups are modified (add, remove, or clear).

    - Updates the cached user data with new group assignments.
    - Publishes an update event to inform dependent services.
    """

    if action in {"post_add", "post_remove", "post_clear"}:
        user_data = build_user_data(instance)

        publish_user_updated_event({"user": user_data, "created": False})
