"""
Constants for authentication message strings.

This class defines messages related to user authentication,
including success and error messages for login operations.
"""

from django.utils.translation import gettext_lazy as _


class MessageConstant:
    SUCCESS_LOGIN = _("Login successful")
