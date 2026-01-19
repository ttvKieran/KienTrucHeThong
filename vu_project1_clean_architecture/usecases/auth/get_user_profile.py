"""
Get User Profile Use Case
Business action: Get user profile information
"""
from typing import Tuple, Optional
from domain.entities import Customer
from domain.exceptions import CustomerNotFoundException
from interfaces.repositories import ICustomerRepository


class GetUserProfileUseCase:
    """
    Use case for getting user profile
    Pure business logic
    """
    
    def __init__(self, customer_repository: ICustomerRepository):
        self.customer_repository = customer_repository
    
    def execute(self, user_id: int) -> Customer:
        """
        Execute use case to get user profile
        
        Args:
            user_id: User ID
            
        Returns:
            Customer profile
            
        Raises:
            CustomerNotFoundException: If customer profile not found
        """
        customer = self.customer_repository.get_by_user_id(user_id)
        
        if customer is None:
            raise CustomerNotFoundException(user_id)
        
        return customer
