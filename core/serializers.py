"""
Serializers for Result Classes

This module contains serializers that transform the result classes into JSON-serializable formats,
which can be returned in API responses.

Classes:
1. ResultSerializer:
   - A base serializer for the Result class, containing the fields 'success' and 'message'.
   - This serializer serves as the foundation for other result serializers.

2. SuccessResultSerializer:
   - Inherits from ResultSerializer.
   - Serializes the SuccessResult class, including 'success' and 'message' fields.

3. ErrorResultSerializer:
   - Inherits from ResultSerializer.
   - Serializes the ErrorResult class, including 'success' and 'message' fields.

4. DataResultSerializer:
   - Inherits from ResultSerializer.
   - Adds a 'data' field, which is serialized as JSON.
   - Contains a validation method for the 'data' field.

5. SuccessDataResultSerializer:
   - Inherits from DataResultSerializer.
   - Serializes the SuccessDataResult class, including 'success', 'message', and 'data' fields.

6. ErrorDataResultSerializer:
   - Inherits from DataResultSerializer.
   - Serializes the ErrorDataResult class, including 'success', 'message', and 'data' fields.
"""

from rest_framework import serializers
from django.contrib.auth.models import Group
from .results import SuccessDataResult, ErrorDataResult, SuccessResult, ErrorResult


class ResultSerializer(serializers.Serializer):
    success = serializers.BooleanField()
    message = serializers.CharField()


class SuccessResultSerializer(ResultSerializer):
    class Meta:
        model = SuccessResult
        fields = ["success", "message"]


class ErrorResultSerializer(ResultSerializer):
    class Meta:
        model = ErrorResult
        fields = ["success", "message"]


class DataResultSerializer(ResultSerializer):
    data = serializers.JSONField()

    def validate_data(self, value):
        return value


class SuccessDataResultSerializer(DataResultSerializer):
    class Meta:
        model = SuccessDataResult
        fields = ["success", "message", "data"]


class ErrorDataResultSerializer(DataResultSerializer):
    class Meta:
        model = ErrorDataResult
        fields = ["success", "message", "data"]
