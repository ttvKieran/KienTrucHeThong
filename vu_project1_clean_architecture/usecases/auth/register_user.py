"""
Register User Use Case
Business action: Register new user with customer profile
"""
from typing import Tuple
from domain.value_objects import UserRegistrationData
from domain.exceptions import UserAlreadyExistsException
from interfaces.repositories import IAuthRepository


class RegisterUserUseCase:
    """
    Use case for user registration
    Pure business logic
    """
    
    def __init__(self, auth_repository: IAuthRepository):
        self.auth_repository = auth_repository
    
    def execute(self, registration_data: UserRegistrationData) -> Tuple[int, int, str]:
        """
        Execute use case to register user
        
        Args:
            registration_data: User registration data
            
        Returns:
            Tuple of (user_id, customer_id, auth_token)
            
        Raises:
            UserAlreadyExistsException: If username already exists
        """
        # Business rule: Check if user already exists
        if self.auth_repository.user_exists(registration_data.username):
            raise UserAlreadyExistsException(registration_data.username)
        
        # Register user
        user_id, customer_id = self.auth_repository.register(registration_data)
        
        # Generate authentication token
        token = self.auth_repository.get_or_create_token(user_id)
        
        return user_id, customer_id, token
