"""
User Service Views
"""
from datetime import datetime
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404

from .models import User, Customer
from .serializers import (
    UserSerializer,
    RegisterSerializer,
    LoginSerializer,
    ProfileUpdateSerializer,
    CustomerSerializer
)
from .auth_utils import generate_jwt_token, get_user_from_token


@api_view(['GET'])
def health_check(request):
    """Health check endpoint"""
    return Response({
        'status': 'healthy',
        'service': 'user-service',
        'timestamp': datetime.now().isoformat()
    })


class RegisterView(APIView):
    """
    User registration endpoint
    POST /api/users/register/
    """
    
    def post(self, request):
        """Register a new user"""
        serializer = RegisterSerializer(data=request.data)
        
        if serializer.is_valid():
            try:
                user = serializer.save()
                token = generate_jwt_token(user)
                
                return Response({
                    'message': 'User registered successfully',
                    'user': UserSerializer(user).data,
                    'token': token
                }, status=status.HTTP_201_CREATED)
                
            except ValueError as e:
                return Response(
                    {'error': str(e)},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class LoginView(APIView):
    """
    User login endpoint
    POST /api/users/login/
    """
    
    def post(self, request):
        """Authenticate user and return JWT token"""
        serializer = LoginSerializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token = generate_jwt_token(user)
            
            return Response({
                'message': 'Login successful',
                'user': UserSerializer(user).data,
                'token': token
            })
        
        return Response(
            serializer.errors,
            status=status.HTTP_401_UNAUTHORIZED
        )


class ProfileView(APIView):
    """
    User profile endpoint
    GET /api/users/profile/ - Get user profile
    PUT /api/users/profile/ - Update user profile
    """
    
    def get(self, request):
        """Get user profile"""
        user_id = get_user_from_token(request)
        
        if not user_id:
            return Response(
                {'error': 'Authentication required'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        user = get_object_or_404(User, id=user_id)
        return Response(UserSerializer(user).data)
    
    def put(self, request):
        """Update user profile"""
        user_id = get_user_from_token(request)
        
        if not user_id:
            return Response(
                {'error': 'Authentication required'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        user = get_object_or_404(User, id=user_id)
        
        # Get or create customer profile
        try:
            customer = user.customer_profile
        except Customer.DoesNotExist:
            return Response(
                {'error': 'Customer profile not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = ProfileUpdateSerializer(data=request.data)
        
        if serializer.is_valid():
            # Update customer profile
            for field, value in serializer.validated_data.items():
                setattr(customer, field, value)
            
            try:
                customer.save()
                return Response({
                    'message': 'Profile updated successfully',
                    'user': UserSerializer(user).data
                })
            except ValueError as e:
                return Response(
                    {'error': str(e)},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class UserDetailView(APIView):
    """
    Get user details by ID (for inter-service communication)
    GET /api/users/{user_id}/
    """
    
    def get(self, request, user_id):
        """Get user details by ID"""
        user = get_object_or_404(User, id=user_id)
        return Response(UserSerializer(user).data)
