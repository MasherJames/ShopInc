
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import (
    AllowAny, IsAuthenticatedOrReadOnly, IsAuthenticated
)
from .serializers import (
    RegisterSerializer, LoginSerializer, UserSerializer
)
from .valiadations import validate_registration


class RegistrationAPIView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    def post(self, request):
        user = request.data
        validate_registration(user)

        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
