""""Views fro User API"""
from rest_framework import generics, authentication, permissions
from rest_framework.settings import api_settings
from rest_framework.authtoken.views import ObtainAuthToken

from user.serializers import (
    AuthTokenSerializer,
    UserSerializer,
)


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer


class CreateTokeView(ObtainAuthToken):
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    # is the user is what it claims to be
    authentication_classes = [authentication.TokenAuthentication]
    # is the user allowed to do what it wants to do
    permission_classes = [permissions.IsAuthenticated]

    # Overriding get_object() method
    def get_object(self):
        return self.request.user
