"""
Serializers for the post API View
"""

from rest_framework import serializers
from core.models import Post

class PostSerializer(serializers.ModelSerializer):
    """Serializer for the Post model."""
    class Meta:
        model = Post
        fields = ['id', 'user', 'title', 'description', 'created_at', 'updated_at']
        read_only_fields = ['user', 'created_at', 'updated_at']
