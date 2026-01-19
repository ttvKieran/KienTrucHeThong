"""
Cart Entity - Domain Model
Represents a shopping cart in the system
"""
from dataclasses import dataclass, field
from typing import Optional, List
from datetime import datetime
from decimal import Decimal


@dataclass
class CartItem:
    """
    CartItem entity representing items in cart
    """
    id: Optional[int]
    book_id: int
    book_title: str
    quantity: int
    price: Decimal
    
    def __post_init__(self):
        """Validate cart item after initialization"""
        self.validate()
    
    def validate(self):
        """Business rules validation for CartItem"""
        if self.quantity <= 0:
            raise ValueError("Cart item quantity must be positive")
        
        if self.price < 0:
            raise ValueError("Cart item price cannot be negative")
    
    def get_subtotal(self) -> Decimal:
        """Calculate subtotal for this cart item"""
        return self.price * self.quantity
    
    def update_quantity(self, new_quantity: int):
        """
        Update quantity with validation
        
        Args:
            new_quantity: New quantity value
            
        Raises:
            ValueError: If quantity is invalid
        """
        if new_quantity <= 0:
            raise ValueError("Quantity must be positive")
        self.quantity = new_quantity


@dataclass
class Cart:
    """
    Cart entity representing shopping cart
    Pure domain object with business logic
    """
    id: Optional[int]
    customer_id: int
    items: List[CartItem] = field(default_factory=list)
    created_at: Optional[datetime] = None
    
    def add_item(self, book_id: int, book_title: str, quantity: int, price: Decimal) -> CartItem:
        """
        Add item to cart or update quantity if exists
        
        Args:
            book_id: Book ID
            book_title: Book title
            quantity: Quantity to add
            price: Price per unit
            
        Returns:
            CartItem: Added or updated cart item
        """
        # Check if book already in cart
        for item in self.items:
            if item.book_id == book_id:
                item.update_quantity(item.quantity + quantity)
                return item
        
        # Create new cart item
        new_item = CartItem(
            id=None,
            book_id=book_id,
            book_title=book_title,
            quantity=quantity,
            price=price
        )
        self.items.append(new_item)
        return new_item
    
    def remove_item(self, book_id: int) -> bool:
        """
        Remove item from cart
        
        Args:
            book_id: Book ID to remove
            
        Returns:
            bool: True if item was removed
        """
        initial_length = len(self.items)
        self.items = [item for item in self.items if item.book_id != book_id]
        return len(self.items) < initial_length
    
    def update_item_quantity(self, book_id: int, quantity: int) -> bool:
        """
        Update quantity of specific item
        
        Args:
            book_id: Book ID
            quantity: New quantity
            
        Returns:
            bool: True if updated successfully
        """
        for item in self.items:
            if item.book_id == book_id:
                item.update_quantity(quantity)
                return True
        return False
    
    def get_item(self, book_id: int) -> Optional[CartItem]:
        """Get cart item by book ID"""
        for item in self.items:
            if item.book_id == book_id:
                return item
        return None
    
    def get_total(self) -> Decimal:
        """Calculate total cart value"""
        return sum(item.get_subtotal() for item in self.items)
    
    def get_total_items(self) -> int:
        """Get total number of items (considering quantities)"""
        return sum(item.quantity for item in self.items)
    
    def is_empty(self) -> bool:
        """Check if cart is empty"""
        return len(self.items) == 0
    
    def clear(self):
        """Remove all items from cart"""
        self.items.clear()
