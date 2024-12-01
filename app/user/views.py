"""
Views for the user API
"""

from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken

from core.models import User

from user.serializers import (
    UserListSerializer,
    UserSerializer,
    AuthTokenSerializer,
    FollowSerializer,
    UnFollowSerializer,
)


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system"""
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user"""
    serializer_class = AuthTokenSerializer


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user"""
    serializer_class = UserSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """Retrieve and return authenticated user"""
        return self.request.user

class ListUsersView(generics.ListAPIView):
    """List all users in the system, excluding the authenticated user"""
    serializer_class = UserListSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Return the list of users, excluding the authenticated user"""
        return User.objects.exclude(id=self.request.user.id)

class FollowUserView(generics.CreateAPIView):
    """Follow another user"""
    serializer_class = FollowSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

class UnFollowUserView(generics.CreateAPIView):
    """Follow another user"""
    serializer_class = UnFollowSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

class FollowersListView(generics.ListAPIView):
    """List all followers of the authenticated user"""
    serializer_class = UserSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Get the authenticated user and return their followers"""
        user = self.request.user
        return user.followers.all()

class FollowingListView(generics.ListAPIView):
    """List all users the authenticated user is following"""
    serializer_class = UserSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Get the authenticated user and return the users they are following"""
        user = self.request.user
        return user.following.all()