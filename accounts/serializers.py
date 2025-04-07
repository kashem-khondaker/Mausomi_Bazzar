from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Profile

User = get_user_model()

class SimpleProfileSerializer(serializers.ModelSerializer):
    """
    সরল প্রোফাইল আপডেটের জন্য Serializer
    """
    class Meta:
        model = Profile
        fields = ['phone', 'address', 'profile_picture']

class ProfileUpdateSerializer(serializers.Serializer):
    """
    ইউজার এবং প্রোফাইল একসাথে আপডেট করার জন্য Serializer
    """
    # User fields
    email = serializers.EmailField(required=False)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    
    # Profile fields
    phone = serializers.CharField(required=False)
    address = serializers.CharField(required=False)
    profile_picture = serializers.ImageField(required=False)

    def update(self, instance, validated_data):
        """
        Update both user and profile data
        """
        user = instance
        profile = user.profile

        # Update user fields
        if 'email' in validated_data:
            user.email = validated_data['email']
        if 'first_name' in validated_data:
            user.first_name = validated_data['first_name']
        if 'last_name' in validated_data:
            user.last_name = validated_data['last_name']
        user.save()

        # Update profile fields
        if 'phone' in validated_data:
            profile.phone = validated_data['phone']
        if 'address' in validated_data:
            profile.address = validated_data['address']
        if 'profile_picture' in validated_data:
            profile.profile_picture = validated_data['profile_picture']
        profile.save()

        return user

class UserSerializer(serializers.ModelSerializer):
    """
    User মডেলের জন্য Serializer
    """
    profile = SimpleProfileSerializer(read_only=True)
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'password', 'profile']
        read_only_fields = ['id']

    def create(self, validated_data):
        """
        Create and return a new user instance
        """
        return User.objects.create_user(**validated_data)

class UserLoginSerializer(serializers.Serializer):
    """
    User লগইন এর জন্য Serializer
    """
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

class UserPasswordChangeSerializer(serializers.Serializer):
    """
    পাসওয়ার্ড পরিবর্তনের জন্য Serializer
    """
    old_password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    new_password = serializers.CharField(write_only=True, style={'input_type': 'password'}, min_length=8)
    confirm_password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    def validate(self, data):
        """
        Check that the passwords match
        """
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError({'confirm_password': "Passwords don't match"})
        return data 