"""
Customer Entity - Domain Model
Represents a customer in the system
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class Customer:
    """
    Customer entity representing system users
    Pure domain object with business logic
    """
    id: Optional[int]
    user_id: int
    fullname: str
    address: str
    phone: str
    note: Optional[str] = None
    
    def __post_init__(self):
        """Validate customer entity after initialization"""
        self.validate()
    
    def validate(self):
        """
        Business rules validation for Customer entity
        """
        if not self.fullname or len(self.fullname.strip()) == 0:
            raise ValueError("Customer fullname cannot be empty")
        
        if not self.address or len(self.address.strip()) == 0:
            raise ValueError("Customer address cannot be empty")
        
        if not self.phone or len(self.phone.strip()) == 0:
            raise ValueError("Customer phone cannot be empty")
        
        # Validate phone format (basic validation)
        if not self.phone.replace('+', '').replace('-', '').replace(' ', '').isdigit():
            raise ValueError("Invalid phone number format")
    
    def update_profile(self, fullname: Optional[str] = None, 
                       address: Optional[str] = None, 
                       phone: Optional[str] = None,
                       note: Optional[str] = None):
        """
        Update customer profile information
        
        Args:
            fullname: New fullname
            address: New address
            phone: New phone
            note: New note
        """
        if fullname:
            self.fullname = fullname
        if address:
            self.address = address
        if phone:
            self.phone = phone
        if note is not None:
            self.note = note
        
        self.validate()
