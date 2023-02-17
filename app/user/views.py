from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from user.serializers import (
    UserSerializer,
    UserProfileSerializer,
    AuthTokenSerializer
)


class CreateUserView(generics.CreateAPIView):
    """Create a new user"""

    serializer_class = UserSerializer


class CreateAuthTokenView(ObtainAuthToken):
    """Create and return a new auth token for user."""

    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class BaseProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = None
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """Retrieve and return the authenticated user."""
        
        return self.request.user


class UserProfileView(BaseProfileView):
    """Manage User Profile"""

    serializer_class = UserProfileSerializer
  

class ManageUserView(BaseProfileView):
    """Manage authenticated user."""

    serializer_class = UserSerializer
 