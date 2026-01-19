"""
Book Entity - Domain Model
Represents a book in the catalog system
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class Book:
    """
    Book entity representing catalog items
    Pure domain object with business logic
    """
    id: Optional[int]
    title: str
    author: str
    stock: int
    note: Optional[str] = None
    slug: Optional[str] = None
    
    def __post_init__(self):
        """Validate book entity after initialization"""
        self.validate()
    
    def validate(self):
        """
        Business rules validation for Book entity
        """
        if not self.title or len(self.title.strip()) == 0:
            raise ValueError("Book title cannot be empty")
        
        if not self.author or len(self.author.strip()) == 0:
            raise ValueError("Book author cannot be empty")
        
        if self.stock < 0:
            raise ValueError("Book stock cannot be negative")
    
    def is_available(self) -> bool:
        """Check if book is available in stock"""
        return self.stock > 0
    
    def has_sufficient_stock(self, quantity: int) -> bool:
        """
        Check if book has sufficient stock for requested quantity
        
        Args:
            quantity: Requested quantity
            
        Returns:
            bool: True if sufficient stock available
        """
        return self.stock >= quantity
    
    def reduce_stock(self, quantity: int):
        """
        Reduce stock by quantity (business logic)
        
        Args:
            quantity: Amount to reduce
            
        Raises:
            ValueError: If insufficient stock
        """
        if not self.has_sufficient_stock(quantity):
            raise ValueError(f"Insufficient stock. Available: {self.stock}, Requested: {quantity}")
        self.stock -= quantity
    
    def increase_stock(self, quantity: int):
        """
        Increase stock by quantity
        
        Args:
            quantity: Amount to add
        """
        if quantity < 0:
            raise ValueError("Quantity must be positive")
        self.stock += quantity
    
    def matches_search(self, search_term: str) -> bool:
        """
        Check if book matches search criteria
        
        Args:
            search_term: Search string
            
        Returns:
            bool: True if title or author contains search term
        """
        search_lower = search_term.lower()
        return (search_lower in self.title.lower() or 
                search_lower in self.author.lower())
