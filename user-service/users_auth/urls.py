from django.urls import path
from .views import LoginView, CustomTokenRefreshView, PermissionVerifyView

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("refresh/", CustomTokenRefreshView.as_view(), name="refresh"),
    path(
        "users/<int:pk>/verify-permission/",
        PermissionVerifyView.as_view(),
        name="verify-permission",
    ),
]
