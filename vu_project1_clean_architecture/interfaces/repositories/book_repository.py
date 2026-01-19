"""
Repository Interfaces
Define contracts for data access
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from domain.entities import Book
from domain.value_objects import SearchCriteria


class IBookRepository(ABC):
    """Interface for Book repository"""
    
    @abstractmethod
    def get_all(self) -> List[Book]:
        """Get all books"""
        pass
    
    @abstractmethod
    def get_by_id(self, book_id: int) -> Optional[Book]:
        """
        Get book by ID
        
        Args:
            book_id: Book ID
            
        Returns:
            Book or None if not found
        """
        pass
    
    @abstractmethod
    def search(self, criteria: SearchCriteria) -> List[Book]:
        """
        Search books based on criteria
        
        Args:
            criteria: Search criteria
            
        Returns:
            List of matching books
        """
        pass
    
    @abstractmethod
    def save(self, book: Book) -> Book:
        """
        Save or update book
        
        Args:
            book: Book entity to save
            
        Returns:
            Saved book with ID
        """
        pass
    
    @abstractmethod
    def delete(self, book_id: int) -> bool:
        """
        Delete book by ID
        
        Args:
            book_id: Book ID
            
        Returns:
            True if deleted successfully
        """
        pass
    
    @abstractmethod
    def update_stock(self, book_id: int, quantity_change: int) -> bool:
        """
        Update book stock
        
        Args:
            book_id: Book ID
            quantity_change: Amount to change (positive or negative)
            
        Returns:
            True if updated successfully
        """
        pass
