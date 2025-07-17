from typing import TypedDict, Type
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status, viewsets
from rest_framework.exceptions import (
    ValidationError as DRFValidationError,
)
from rest_framework.permissions import BasePermission
from rest_framework.response import Response
from rest_framework.views import exception_handler, APIView
from .constants import MessageConstant, ErrorConstant, CacheConstant
from .decorators import cacheable, cache_update, cache_invalidate
from .results import ErrorResult, SuccessResult, SuccessDataResult
from .serializers import (
    ErrorResultSerializer,
    SuccessDataResultSerializer,
    SuccessResultSerializer,
)
from .utils import SerializerUtil


class CustomResponseMixin:
    def success_response(self, message=None, status_code=status.HTTP_200_OK):
        return Response(
            SuccessResultSerializer(SuccessResult(message=message)).data,
            status=status_code,
        )

    def error_response(
        self,
        message=MessageConstant.ERROR_SERVICE_REQUEST,
        status_code=status.HTTP_400_BAD_REQUEST,
    ):
        return Response(
            ErrorResultSerializer(ErrorResult(message=message)).data, status=status_code
        )

    def success_data_response(
        self, data=None, message=None, status_code=status.HTTP_200_OK
    ):
        return Response(
            SuccessDataResultSerializer(
                SuccessDataResult(data=data, message=message)
            ).data,
            status=status_code,
        )


class ActionPermissionRule(TypedDict):
    action: str
    permissions: list[Type[BasePermission]]


class BaseModelViewSet(CustomResponseMixin, viewsets.ModelViewSet):
    permissions: list[ActionPermissionRule] = []
    success_create_message = MessageConstant.SUCCESS_CREATE
    success_update_message = MessageConstant.SUCCESS_UPDATE
    success_delete_message = MessageConstant.SUCCESS_DELETE
    success_listed_message = MessageConstant.SUCCESS_LIST
    success_retrieved_message = MessageConstant.SUCCESS_RETRIEVE
    cache_service_name = None

    def get_permissions(self):
        for rule in self.permissions:
            if rule.get("action") == self.action:
                return [perm() for perm in rule.get("permissions", [])]

        return [permission() for permission in self.permission_classes]

    def handle_action(self, action, *args, **kwargs):
        try:
            return action(*args, **kwargs)
        except Exception as e:
            return self.handle_exception(e)

    def handle_exception(self, exc):
        if isinstance(exc, ObjectDoesNotExist):
            return self.error_response(
                MessageConstant.NOT_MATCH_ANY_RECORD,
                status_code=ErrorConstant.NOT_FOUND_STATUS_CODE,
            )

        response = exception_handler(exc, self.get_exception_handler_context())

        if response is not None:
            if isinstance(exc, DRFValidationError) and isinstance(response.data, dict):
                formatted_errors = SerializerUtil.get_error_messages(response.data)

                return self.error_response(
                    formatted_errors, status_code=response.status_code
                )

            # Set default error message for other exceptions
            return self.error_response(str(exc), status_code=response.status_code)

        return super().handle_exception(exc)

    @cache_update()
    def create(self, request, *args, **kwargs):
        response = self.handle_action(super().create, request, *args, **kwargs)

        return self.success_data_response(
            response.data,
            message=self.success_create_message,
            status_code=response.status_code,
        )

    @cache_update()
    def update(self, request, *args, **kwargs):
        response = self.handle_action(super().update, request, *args, **kwargs)

        return self.success_data_response(
            response.data,
            message=self.success_update_message,
            status_code=response.status_code,
        )

    @cache_invalidate(type=CacheConstant.TYPE_MODEL)
    def destroy(self, request, *args, **kwargs):
        response = self.handle_action(super().destroy, request, *args, **kwargs)

        return self.success_response(
            message=self.success_delete_message, status_code=response.status_code
        )

    @cacheable(type=CacheConstant.TYPE_ENDPOINT, timeout=CacheConstant.TIMEOUT_SHORT)
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)

        return self.success_data_response(
            response.data,
            message=self.success_listed_message,
            status_code=response.status_code,
        )

    @cacheable(type=CacheConstant.TYPE_MODEL)
    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)

        return self.success_data_response(
            response.data,
            message=self.success_retrieved_message,
            status_code=response.status_code,
        )


class BaseAPIView(APIView, CustomResponseMixin):
    def handle_exception(self, exc):
        if isinstance(exc, ObjectDoesNotExist):
            return self.error_response(
                MessageConstant.NOT_MATCH_ANY_RECORD,
                status_code=ErrorConstant.NOT_FOUND_STATUS_CODE,
            )

        response = exception_handler(exc, self.get_exception_handler_context())

        if response is not None:
            if isinstance(exc, DRFValidationError) and isinstance(response.data, dict):
                formatted_errors = SerializerUtil.get_error_messages(response.data)
                return self.error_response(
                    formatted_errors, status_code=response.status_code
                )

            return self.error_response(str(exc), status_code=response.status_code)

        return super().handle_exception(exc)
