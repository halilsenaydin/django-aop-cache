from rest_framework import serializers
from django.contrib.auth.models import Group
from .models import User


class GroupSerializer(serializers.ModelSerializer):
    """
    Serializer for Django's built-in Group model.

    This is used to represent user groups with basic fields (id and name),
    typically for displaying group info in user-related APIs.
    """

    class Meta:
        model = Group
        fields = ["id", "name"]


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the custom User model.

    This serializer handles:
    - Creating and updating user instances, including secure password handling.
    - Assigning and displaying user groups.
    - Separating read-only group details (`group_details`) from writable group assignment (`groups`).

    Notes:
    - `password` is write-only and hashed using `set_password`.
    - `group_details` is populated with nested group data for readability.
    - `groups` expects a list of group IDs for assignment.
    """

    group_details = GroupSerializer(source="groups", many=True, read_only=True)
    groups = serializers.PrimaryKeyRelatedField(
        queryset=Group.objects.all(),
        many=True,
        write_only=True,
        required=False,
    )

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "is_active",
            "password",
            "groups",
            "group_details",
        ]
        extra_kwargs = {"password": {"write_only": True}}
        read_only_fields = ["id"]

    def create(self, validated_data):
        password = validated_data.pop("password")
        groups = validated_data.pop("groups", [])
        user = User(**validated_data)

        user.set_password(password)
        user.save()

        # Assign groups to the user
        user.groups.set(groups)

        return user

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        groups = validated_data.pop("groups", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)

        instance.save()

        if groups is not None:
            instance.groups.set(groups)

        return instance
