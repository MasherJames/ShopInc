
from django.conf import settings
from django.core.mail import send_mail
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import (
    AllowAny, IsAuthenticatedOrReadOnly, IsAuthenticated
)
from .serializers import (
    RegisterSerializer, LoginSerializer, UserSerializer
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
