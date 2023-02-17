from rest_framework import serializers
from django.contrib.auth import (
    get_user_model,
    authenticate
)

from core.models import UserProfile

from django.utils.translation import gettext_lazy as _

from django.core.exceptions import ObjectDoesNotExist


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object."""

    class Meta:
        model = get_user_model()
        fields = ['email', 'name', 'password']
        extra_kwargs = {
            'password': {
                'write_only': True,
                'min_length': 8
            }
        }
    
    def create(self, validated_data):
        """Create and return a new user with encrypted password."""

        return get_user_model().objects.create_user(**validated_data)
    
    def update(self, instance, validated_data):
        """Update and return a user."""

        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()
        
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for user profile model."""

    class Meta:
        model = UserProfile
        exclude = ('id', 'auth_user',)

    
    def update(self, instance, validated_data):
        user_profile = UserProfile.objects.get(
            auth_user=instance
        )  
        user_profile.first_name = validated_data['first_name']
        user_profile.last_name = validated_data['last_name']
        user_profile.cohort_number = validated_data['cohort_number']
        user_profile.save()
        return user_profile
    
       



class AuthTokenSerializer(serializers.Serializer):
    """Serializer for user auth tokens."""

    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        """Validate and authenticate a user."""

        email = attrs.get('email')
        password= attrs.get('password')
        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password
        )

        if not user:
            msg = _('Unable to authenticate user with provided credentials')
            raise serializers.ValidationError(msg, code='authorization')
        
        attrs['user'] = user
        return attrs
