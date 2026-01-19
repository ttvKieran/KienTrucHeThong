"""
Login User Use Case
Business action: Authenticate user and generate token
"""
from typing import Tuple
from domain.value_objects import UserCredentials
from domain.exceptions import InvalidCredentialsException
from interfaces.repositories import IAuthRepository


class LoginUserUseCase:
    """
    Use case for user login
    Pure business logic
    """
    
    def __init__(self, auth_repository: IAuthRepository):
        self.auth_repository = auth_repository
    
    def execute(self, credentials: UserCredentials) -> Tuple[int, str]:
        """
        Execute use case to login user
        
        Args:
            credentials: User credentials
            
        Returns:
            Tuple of (user_id, auth_token)
            
        Raises:
            InvalidCredentialsException: If credentials are invalid
        """
        # Authenticate user
        user_id = self.auth_repository.authenticate(credentials)
        
        if user_id is None:
            raise InvalidCredentialsException()
        
        # Generate authentication token
        token = self.auth_repository.get_or_create_token(user_id)
        
        return user_id, token
