from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .serializers import (
    UserSerializer,
    SimpleProfileSerializer,
    ProfileUpdateSerializer,
    UserLoginSerializer,
    UserPasswordChangeSerializer
)

def get_tokens_for_user(user):
    """Helper function to generate JWT tokens"""
    refresh = RefreshToken.for_user(user)
    return {
        'user': UserSerializer(user).data,
        'refresh': str(refresh),
        'access': str(refresh.access_token)
    }

class RegisterAPIView(generics.CreateAPIView):
    """
    User রেজিস্ট্রেশন API
    """
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(get_tokens_for_user(user), status=status.HTTP_201_CREATED)

class LoginAPIView(generics.GenericAPIView):
    """
    User লগইন API
    """
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(**serializer.validated_data)
        if not user:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(get_tokens_for_user(user))

class UserProfileView(generics.RetrieveAPIView):
    """
    User প্রোফাইল দেখানোর API
    """
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

class UpdateProfileView(generics.UpdateAPIView):
    """
    Profile তথ্য আপডেট করার API
    """
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileUpdateSerializer

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        # Return updated user data
        return Response(UserSerializer(instance).data)

class ChangePasswordAPIView(generics.GenericAPIView):
    """
    পাসওয়ার্ড পরিবর্তনের API
    """
    permission_classes = [IsAuthenticated]
    serializer_class = UserPasswordChangeSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if not request.user.check_password(serializer.validated_data['old_password']):
            return Response({'error': 'Invalid old password'}, status=status.HTTP_400_BAD_REQUEST)
        request.user.set_password(serializer.validated_data['new_password'])
        request.user.save()
        return Response({'message': 'Password changed successfully'})
