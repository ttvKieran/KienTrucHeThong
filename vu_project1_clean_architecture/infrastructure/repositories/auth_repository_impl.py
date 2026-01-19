"""
Auth Repository Implementation
Infrastructure layer - implements repository interface using Django Auth
"""
from typing import Optional, Tuple
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from domain.value_objects import UserCredentials, UserRegistrationData
from domain.exceptions import UserAlreadyExistsException
from interfaces.repositories import IAuthRepository
from infrastructure.models import CustomerModel


class DjangoAuthRepository(IAuthRepository):
    """
    Django Auth implementation of Auth repository
    """
    
    def authenticate(self, credentials: UserCredentials) -> Optional[int]:
        """Authenticate user"""
        user = authenticate(
            username=credentials.username,
            password=credentials.password
        )
        
        if user is not None:
            return user.id
        
        return None
    
    def register(self, registration_data: UserRegistrationData) -> Tuple[int, int]:
        """Register new user with customer profile"""
        # Check if user exists
        if User.objects.filter(username=registration_data.username).exists():
            raise UserAlreadyExistsException(registration_data.username)
        
        # Create user
        user = User.objects.create_user(
            username=registration_data.username,
            email=registration_data.email or '',
            password=registration_data.password,
            first_name=registration_data.first_name or '',
            last_name=registration_data.last_name or ''
        )
        
        # Create customer profile
        customer = CustomerModel.objects.create(
            user=user,
            fullname=registration_data.fullname,
            address=registration_data.address,
            phone=registration_data.phone,
            note=registration_data.note or ''
        )
        
        return user.id, customer.id
    
    def user_exists(self, username: str) -> bool:
        """Check if user exists"""
        return User.objects.filter(username=username).exists()
    
    def get_or_create_token(self, user_id: int) -> str:
        """Get or create authentication token"""
        user = User.objects.get(id=user_id)
        token, created = Token.objects.get_or_create(user=user)
        return token.key
