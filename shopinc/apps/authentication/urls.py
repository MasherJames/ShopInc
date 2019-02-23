from django.urls import path
from .views import (
    RegistrationAPIView, LoginAPIView, PasswordResetAPIView,
    PasswordUpdateAPIView
)

urlpatterns = [
    path('users/register/', RegistrationAPIView.as_view()),
    path('users/login/', LoginAPIView.as_view()),
    path('users/reset_password/', PasswordResetAPIView.as_view()),
    path('users/update_password/<token>', PasswordUpdateAPIView.as_view())
]
