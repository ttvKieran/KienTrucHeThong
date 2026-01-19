"""
Cart Repository Interface
"""
from abc import ABC, abstractmethod
from typing import Optional
from domain.entities import Cart, CartItem


class ICartRepository(ABC):
    """Interface for Cart repository"""
    
    @abstractmethod
    def get_by_customer_id(self, customer_id: int) -> Optional[Cart]:
        """
        Get cart by customer ID
        
        Args:
            customer_id: Customer ID
            
        Returns:
            Cart or None if not found
        """
        pass
    
    @abstractmethod
    def get_by_id(self, cart_id: int) -> Optional[Cart]:
        """
        Get cart by ID
        
        Args:
            cart_id: Cart ID
            
        Returns:
            Cart or None if not found
        """
        pass
    
    @abstractmethod
    def save(self, cart: Cart) -> Cart:
        """
        Save or update cart
        
        Args:
            cart: Cart entity to save
            
        Returns:
            Saved cart with ID
        """
        pass
    
    @abstractmethod
    def save_item(self, cart_id: int, item: CartItem) -> CartItem:
        """
        Save or update cart item
        
        Args:
            cart_id: Cart ID
            item: Cart item to save
            
        Returns:
            Saved cart item with ID
        """
        pass
    
    @abstractmethod
    def delete_item(self, cart_id: int, book_id: int) -> bool:
        """
        Delete cart item
        
        Args:
            cart_id: Cart ID
            book_id: Book ID
            
        Returns:
            True if deleted successfully
        """
        pass
    
    @abstractmethod
    def clear(self, cart_id: int) -> bool:
        """
        Clear all items from cart
        
        Args:
            cart_id: Cart ID
            
        Returns:
            True if cleared successfully
        """
        pass
