from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from drf_yasg.utils import swagger_auto_schema
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.permissions import AllowAny
from core.constants import MessageConstant as CoreMessageConstant
from core.views import BaseAPIView, CustomResponseMixin
from core.utils import SerializerUtil
from users.serializers import UserSerializer
from .constants import MessageConstant
from .serializers import LoginSerializer, PermissionVerifySerializer

User = get_user_model()


class CustomTokenRefreshView(TokenRefreshView, CustomResponseMixin):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except Exception:
            return self.error_response(message=CoreMessageConstant.UNAUTHORIZED)

        data = serializer.validated_data

        return self.success_data_response(
            data=data, message=MessageConstant.SUCCESS_LOGIN
        )


@method_decorator(csrf_exempt, name="dispatch")
class LoginView(BaseAPIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(request_body=LoginSerializer)
    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            username = serializer.validated_data["username"]
            password = serializer.validated_data["password"]
            user = authenticate(username=username, password=password)

            if user is not None:
                refresh = RefreshToken.for_user(user)
                user_data = UserSerializer(user).data

                return self.success_data_response(
                    data={
                        "refresh": str(refresh),
                        "access": str(refresh.access_token),
                        "user": user_data,
                    },
                    message=MessageConstant.SUCCESS_LOGIN,
                )

            return self.error_response(message=CoreMessageConstant.UNAUTHORIZED)

        errors = SerializerUtil.get_error_messages(serializer.errors)

        return self.error_response(message=errors)


class PermissionVerifyView(BaseAPIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(request_body=PermissionVerifySerializer)
    def post(self, request, pk):
        serializer = PermissionVerifySerializer(data=request.data)

        if not serializer.is_valid():
            return self.error_response(message=serializer.errors)

        user = self._get_user(pk)

        if not user:
            return self.error_response(
                message=CoreMessageConstant.NOT_MATCH_ANY_RECORD, status_code=404
            )

        self.check_object_permissions(request, user)

        has_access = self._check_user_access(
            user=user,
            required_groups=serializer.validated_data.get("required_groups", []),
            required_permissions=serializer.validated_data.get(
                "required_permissions", []
            ),
        )

        return self.success_data_response(data=has_access)

    def _get_user(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            return None

    def _check_user_access(self, user, required_groups, required_permissions):
        return self._is_in_required_groups(
            user, required_groups
        ) and self._has_required_permissions(user, required_permissions)

    def _is_in_required_groups(self, user, required_groups):
        if not required_groups:
            return True

        user_groups = set(user.groups.values_list("name", flat=True))

        return bool(user_groups.intersection(required_groups))

    def _has_required_permissions(self, user, required_permissions):
        if not required_permissions:
            return True

        return all(user.has_perm(perm) for perm in required_permissions)
