
import jwt
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import (
    AllowAny, IsAuthenticatedOrReadOnly, IsAuthenticated
)
from .models import User
from .serializers import (
    RegisterSerializer, LoginSerializer, UserSerializer, PasswordSerializer
)
from .valiadations import validate_registration, validate_login


class RegistrationAPIView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    def post(self, request):
        user = request.data
        validate_registration(user)

        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # RegistrationAPIView.send_email(user)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @staticmethod
    def send_email(user):
        try:
            subject = "Thanks for using chosing shopinc"
            body = "Shop at your pace and get the best products"
            recipient = user['email']
            sender = settings.EMAIL_HOST_USER
            send_mail(subject, body, sender, [
                recipient], fail_silently=True)
        except:
            print("failed")


class LoginAPIView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request):
        data = request.data
        validate_login(data)

        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class PasswordResetAPIView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer

    def post(self, request):
        data = request.data['email']

        if not data:
            return Response(
                {"Message": "Please provide your email for password reset"},
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            user = User.objects.get(email=data)
            token = PasswordResetAPIView.generate_password_reset_token(data)

            serializer = self.serializer_class(user)
            subject = "Password Reset"
            body = "Click this link to reset your password" + \
                f"http://{get_current_site(request)}/api/users/update_password/{token}"
            recipient = [serializer['email'].value, ]
            sender = settings.EMAIL_HOST_USER
            send_mail(subject, body, sender,
                      recipient, fail_silently=True)

            return Response(
                {"Message": "Check your email for password reset link", "token": token},
                status=status.HTTP_201_CREATED)

        except:
            return Response({"Message": "User not found"},
                            status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def generate_password_reset_token(data):
        token = jwt.encode({
            'email': data
        }, settings.SECRET_KEY, algorithm="HS256")

        return token.decode('utf-8')


class PasswordUpdateAPIView(generics.UpdateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = PasswordSerializer
    # The URL conf should include a keyword argument corresponding to this value
    lookup_url_kwarg = 'token'

    def update(self, request, *args, **kwargs):
        token = self.kwargs.get(self.lookup_url_kwarg)
        new_password = request.data.get('new_password')

        if not new_password:
            return Response({"Message": "New password is required"},
                            status=status.HTTP_404_NOT_FOUND)

        try:
            decoded_token = jwt.decode(
                token, settings.SECRET_KEY, algorithms=['HS256']
            )
            user = User.objects.get(email=decoded_token['email'])
            user.set_password(new_password)
            user.save()

            return Response({"Message": "Password successfully reset"},
                            status=status.HTTP_201_CREATED)
        except:
            return Response({"Message": "Password could not be reset"},
                            status=status.HTTP_400_BAD_REQUEST)
