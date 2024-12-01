"""
Views for the post API
"""

from rest_framework import (
    viewsets,
    authentication,
    permissions,
    status,
)
from rest_framework.response import Response

from core.models import Post
from post.serializers import PostSerializer

class PostViewSet(viewsets.ModelViewSet):
    """Post viewset to handle creation and listing of posts."""
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        """Filter posts to include only the authenticated user and their followers' posts."""
        user = self.request.user
        following_users = user.following.all()
        return Post.objects.filter(user__in=[user] + list(following_users))

    def perform_create(self, serializer):
        """Set the user of the post to the currently authenticated user."""
        serializer.save(user=self.request.user)
    
    def update(self, request, *args, **kwargs):
        """Ensure the user can only update their own posts."""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        if instance.user != request.user:
            return Response(
                {'detail': 'You do not have permission to update this post.'},
                status=status.HTTP_403_FORBIDDEN,
            )
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        """Ensure the user can only delete their own posts."""
        instance = self.get_object()
        if instance.user != request.user:
            return Response(
                {'detail': 'You do not have permission to delete this post.'},
                status=status.HTTP_403_FORBIDDEN,
            )
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)