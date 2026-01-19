from django.contrib.auth import login, logout
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from ..serializers import RegisterSerializer, LoginSerializer, UserSerializer, CustomerSerializer
from ..services.auth_service import AuthService


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    """
    API endpoint for user registration
    POST /api/auth/register
    """
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        try:
            # Use service layer for business logic
            user, token, customer = AuthService.register_user(serializer.validated_data)
            
            return Response({
                'message': 'User registered successfully',
                'token': token.key,
                'user': UserSerializer(user).data,
                'customer': CustomerSerializer(customer).data
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def user_login(request):
    """
    API endpoint for user login
    POST /api/auth/login
    """
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        
        # Use service layer for authentication
        user = AuthService.authenticate_user(username, password)
        
        if user is not None:
            login(request, user)
            token = AuthService.get_or_create_token(user)
            
            # Get user profile using service
            _, customer = AuthService.get_user_profile(user)
            customer_data = CustomerSerializer(customer).data if customer else None
            
            return Response({
                'message': 'Login successful',
                'token': token.key,
                'user': UserSerializer(user).data,
                'customer': customer_data
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'error': 'Invalid username or password'
            }, status=status.HTTP_401_UNAUTHORIZED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_logout(request):
    """
    API endpoint for user logout
    POST /api/auth/logout
    """
    try:
        # Use service layer for logout
        AuthService.logout_user(request.user)
        logout(request)
        return Response({
            'message': 'Logout successful'
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_profile(request):
    """
    API endpoint to get current user profile
    GET /api/auth/profile
    """
    # Use service layer to get profile
    user, customer = AuthService.get_user_profile(request.user)
    
    return Response({
        'user': UserSerializer(user).data,
        'customer': CustomerSerializer(customer).data if customer else None
    }, status=status.HTTP_200_OK)
