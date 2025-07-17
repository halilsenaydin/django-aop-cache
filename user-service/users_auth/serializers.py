"""
Serializers for authentication and permission verification in the user_service.

This module defines serializer classes used for:
- Handling login requests by validating username and password.
- Validating group and permission-based access control in views.

Serializers:
- LoginSerializer: Validates user credentials (username and password).
- PermissionVerifySerializer: Accepts optional lists of required groups and permissions
  to verify access rights.

These serializers are typically used in authentication views or permission-checking endpoints.
"""

from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class PermissionVerifySerializer(serializers.Serializer):
    required_groups = serializers.ListField(
        child=serializers.CharField(), required=False
    )
    required_permissions = serializers.ListField(
        child=serializers.CharField(), required=False
    )
