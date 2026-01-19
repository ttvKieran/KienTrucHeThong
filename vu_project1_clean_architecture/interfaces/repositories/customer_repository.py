"""
Customer Repository Interface
"""
from abc import ABC, abstractmethod
from typing import Optional
from domain.entities import Customer


class ICustomerRepository(ABC):
    """Interface for Customer repository"""
    
    @abstractmethod
    def get_by_id(self, customer_id: int) -> Optional[Customer]:
        """
        Get customer by ID
        
        Args:
            customer_id: Customer ID
            
        Returns:
            Customer or None if not found
        """
        pass
    
    @abstractmethod
    def get_by_user_id(self, user_id: int) -> Optional[Customer]:
        """
        Get customer by user ID
        
        Args:
            user_id: User ID
            
        Returns:
            Customer or None if not found
        """
        pass
    
    @abstractmethod
    def save(self, customer: Customer) -> Customer:
        """
        Save or update customer
        
        Args:
            customer: Customer entity to save
            
        Returns:
            Saved customer with ID
        """
        pass
    
    @abstractmethod
    def delete(self, customer_id: int) -> bool:
        """
        Delete customer by ID
        
        Args:
            customer_id: Customer ID
            
        Returns:
            True if deleted successfully
        """
        pass
