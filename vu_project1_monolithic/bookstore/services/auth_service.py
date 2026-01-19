"""
Authentication Service - Business Logic Layer
Handles user registration, login, and profile management
"""
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from ..models import Customer


class AuthService:
    """Service class for authentication operations"""
    
    @staticmethod
    def register_user(validated_data):
        """
        Register a new user with customer profile
        
        Args:
            validated_data: Dictionary containing user and customer data
            
        Returns:
            tuple: (user, token, customer)
            
        Raises:
            Exception: If user creation fails
        """
        # Extract customer data
        fullname = validated_data.pop('fullname')
        address = validated_data.pop('address')
        phone = validated_data.pop('phone')
        note = validated_data.pop('note', '')
        validated_data.pop('password2')
        
        # Create user
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        
        # Create customer profile
        customer = Customer.objects.create(
            user=user,
            fullname=fullname,
            address=address,
            phone=phone,
            note=note
        )
        
        # Generate token
        token, created = Token.objects.get_or_create(user=user)
        
        return user, token, customer
    
    @staticmethod
    def authenticate_user(username, password):
        """
        Authenticate user credentials
        
        Args:
            username: User's username
            password: User's password
            
        Returns:
            User object if authentication successful, None otherwise
        """
        return authenticate(username=username, password=password)
    
    @staticmethod
    def get_or_create_token(user):
        """
        Get existing token or create new one for user
        
        Args:
            user: User object
            
        Returns:
            Token object
        """
        token, created = Token.objects.get_or_create(user=user)
        return token
    
    @staticmethod
    def get_user_profile(user):
        """
        Get user profile with customer information
        
        Args:
            user: User object
            
        Returns:
            tuple: (user, customer or None)
        """
        try:
            customer = Customer.objects.get(user=user)
            return user, customer
        except Customer.DoesNotExist:
            return user, None
    
    @staticmethod
    def logout_user(user):
        """
        Logout user by deleting their token
        
        Args:
            user: User object
            
        Returns:
            bool: True if successful
        """
        try:
            user.auth_token.delete()
            return True
        except Exception as e:
            raise Exception(f"Logout failed: {str(e)}")
