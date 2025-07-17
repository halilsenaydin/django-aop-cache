from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import AllowAny
from core.constants import ConfigConstant as CoreConfigConstant
from core.views import BaseModelViewSet
from .models import User
from .serializers import (
    UserSerializer,
)


class UserViewSet(BaseModelViewSet):
    """
    ViewSet for managing User instances.

    Supports all standard CRUD operations:
        - list: Retrieve users.
        - retrieve: Get user details.
        - create: Create new user with roles and password handling.
        - update/partial_update: Update user data, roles, and password.
        - destroy: Delete user.

    Uses UserSerializer for all operations.
    """

    cache_service_name = CoreConfigConstant.USER_SERVICE_NAME
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [AllowAny]
