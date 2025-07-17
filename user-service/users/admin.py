from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model

User = get_user_model()


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ("username", "email", "first_name", "last_name", "is_staff")
    list_filter = ("is_staff", "is_superuser", "groups")
    search_fields = ("username", "email", "first_name", "last_name")

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Personal Informations", {"fields": ("first_name", "last_name", "email")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        ("Important Date", {"fields": ("last_login", "date_joined")}),
    )

    filter_horizontal = ("groups", "user_permissions")
