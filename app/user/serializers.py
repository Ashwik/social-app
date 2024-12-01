"""
Serializers for the user API View
"""

from django.contrib.auth import (
    get_user_model,
    authenticate,
)

from django.utils.translation import gettext as _
from django.core.exceptions import ValidationError

from rest_framework import serializers
from core.models import User


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object"""

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'fullname', 'password']
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        """Create a new user with encrypted password and return it"""
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update a user, setting the password correctly and return it"""
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user authentication object"""
    username = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=True
    )

    def validate(self, attrs):
        """Validate and authenticate the user"""
        username = attrs.get('username')
        password = attrs.get('password')
        user = authenticate(
            request=self.context.get('request'),
            username=username,
            password=password,
        )

        if not user:
            msg = _('Unable to authenticate with provided credentials')
            raise serializers.ValidationError(msg, code='authentication')

        attrs['user'] = user
        return attrs


class UserListSerializer(serializers.ModelSerializer):
    """Serializer to represent a user for listing purposes"""

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'fullname'] 

class FollowSerializer(serializers.Serializer):
    username = serializers.CharField()

    def validate_username(self, value):
        """Validate that the user to follow exists."""
        try:
            user_to_follow = User.objects.get(username=value)
        except User.DoesNotExist:
            raise ValidationError("User not found.")
        return user_to_follow

    def validate(self, attrs):
        """Ensure the user is not following themselves."""
        user_to_follow = attrs.get('username')
        if user_to_follow == self.context['request'].user:
            raise ValidationError("You cannot follow yourself.")
        return attrs

    def create(self, validated_data):
        """Add the user to the following list."""
        user_to_follow = validated_data['username']
        user = self.context['request'].user

        if user_to_follow in user.following.all():
            raise ValidationError(f"You are already following {user_to_follow.username}.")
        
        user.following.add(user_to_follow)
        return user_to_follow


class UnFollowSerializer(serializers.Serializer):
    username = serializers.CharField()

    def validate_username(self, value):
        """Validate that the user to unfollow exists."""
        try:
            user_to_unfollow = User.objects.get(username=value)
        except User.DoesNotExist:
            raise ValidationError("User not found.")
        return user_to_unfollow

    def validate(self, attrs):
        """Ensure the user is not unfollowing themselves."""
        user_to_unfollow = attrs.get('username')
        if user_to_unfollow == self.context['request'].user:
            raise ValidationError("You cannot unfollow yourself.")
        return attrs

    def create(self, validated_data):
        """Remove the user from the following list if they are following."""
        user_to_unfollow = validated_data['username']
        user = self.context['request'].user

        if user_to_unfollow not in user.following.all():
            raise ValidationError(f"You are not following {user_to_unfollow.username}.")

        user.following.remove(user_to_unfollow)
        return user_to_unfollow