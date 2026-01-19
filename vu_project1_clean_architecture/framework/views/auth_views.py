"""
Auth Views
Framework layer - controllers that handle HTTP requests
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from domain.value_objects import UserCredentials, UserRegistrationData
from domain.exceptions import (
    InvalidCredentialsException,
    UserAlreadyExistsException,
    CustomerNotFoundException
)
from usecases.auth import RegisterUserUseCase, LoginUserUseCase, GetUserProfileUseCase
from framework.dependencies import inject_dependencies


@inject_dependencies
class RegisterView(APIView):
    """
    Controller for user registration
    """
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.register_use_case = None  # Will be injected
    
    def post(self, request):
        """
        POST /api/auth/register/
        Body: {username, password, email, first_name, last_name, fullname, address, phone, note}
        """
        try:
            # Extract and validate data
            registration_data = UserRegistrationData(
                username=request.data.get('username'),
                password=request.data.get('password'),
                email=request.data.get('email'),
                first_name=request.data.get('first_name'),
                last_name=request.data.get('last_name'),
                fullname=request.data.get('fullname'),
                address=request.data.get('address'),
                phone=request.data.get('phone'),
                note=request.data.get('note')
            )
            
            # Execute use case
            user_id, customer_id, token = self.register_use_case.execute(registration_data)
            
            return Response({
                'user_id': user_id,
                'customer_id': customer_id,
                'token': token,
                'message': 'User registered successfully'
            }, status=status.HTTP_201_CREATED)
        
        except UserAlreadyExistsException as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except ValueError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


@inject_dependencies
class LoginView(APIView):
    """
    Controller for user login
    """
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.login_use_case = None  # Will be injected
    
    def post(self, request):
        """
        POST /api/auth/login/
        Body: {username, password}
        """
        try:
            # Extract credentials
            credentials = UserCredentials(
                username=request.data.get('username'),
                password=request.data.get('password')
            )
            
            # Execute use case
            user_id, token = self.login_use_case.execute(credentials)
            
            return Response({
                'user_id': user_id,
                'token': token,
                'message': 'Login successful'
            }, status=status.HTTP_200_OK)
        
        except InvalidCredentialsException as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_401_UNAUTHORIZED
            )
        except ValueError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

@inject_dependencies

class ProfileView(APIView):
    """
    Controller for user profile
    """
    permission_classes = [IsAuthenticated]
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.get_profile_use_case = None  # Will be injected
    
    def get(self, request):
        """GET /api/auth/profile/"""
        try:
            user_id = request.user.id
            
            # Execute use case
            customer = self.get_profile_use_case.execute(user_id)
            
            # Convert entity to response format
            from framework.serializers import CustomerSerializer
            serializer = CustomerSerializer(customer)
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except CustomerNotFoundException as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
