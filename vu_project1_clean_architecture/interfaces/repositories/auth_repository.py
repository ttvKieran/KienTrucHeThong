"""
Authentication Repository Interface
"""
from abc import ABC, abstractmethod
from typing import Optional, Tuple
from domain.value_objects import UserCredentials, UserRegistrationData


class IAuthRepository(ABC):
    """Interface for authentication operations"""
    
    @abstractmethod
    def authenticate(self, credentials: UserCredentials) -> Optional[int]:
        """
        Authenticate user
        
        Args:
            credentials: User credentials
            
        Returns:
            User ID if authentication successful, None otherwise
        """
        pass
    
    @abstractmethod
    def register(self, registration_data: UserRegistrationData) -> Tuple[int, int]:
        """
        Register new user with customer profile
        
        Args:
            registration_data: User registration data
            
        Returns:
            Tuple of (user_id, customer_id)
            
        Raises:
            UserAlreadyExistsException: If username already exists
        """
        pass
    
    @abstractmethod
    def user_exists(self, username: str) -> bool:
        """
        Check if user exists
        
        Args:
            username: Username to check
            
        Returns:
            True if user exists
        """
        pass
    
    @abstractmethod
    def get_or_create_token(self, user_id: int) -> str:
        """
        Get or create authentication token
        
        Args:
            user_id: User ID
            
        Returns:
            Authentication token
        """
        pass
