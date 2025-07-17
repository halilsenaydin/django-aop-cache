from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    Custom User model extending Django's built-in AbstractUser.

    This model preserves all default fields and authentication behaviors, while allowing
    for future customization — such as adding profile data, roles, or other business-specific attributes.

    Currently, it overrides the __str__ method to return the username.
    """

    def __str__(self):
        return self.username
