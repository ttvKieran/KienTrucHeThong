"""
Value Objects for Domain Layer
Immutable objects that represent domain concepts
"""
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class UserCredentials:
    """Value object for user authentication credentials"""
    username: str
    password: str
    
    def __post_init__(self):
        if not self.username or len(self.username.strip()) == 0:
            raise ValueError("Username cannot be empty")
        if not self.password or len(self.password) < 6:
            raise ValueError("Password must be at least 6 characters")


@dataclass(frozen=True)
class UserRegistrationData:
    """Value object for user registration"""
    username: str
    password: str
    email: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    fullname: str
    address: str
    phone: str
    note: Optional[str] = None
    
    def __post_init__(self):
        if not self.username or len(self.username.strip()) == 0:
            raise ValueError("Username cannot be empty")
        if not self.password or len(self.password) < 6:
            raise ValueError("Password must be at least 6 characters")
        if not self.fullname or len(self.fullname.strip()) == 0:
            raise ValueError("Fullname cannot be empty")
        if not self.address or len(self.address.strip()) == 0:
            raise ValueError("Address cannot be empty")
        if not self.phone or len(self.phone.strip()) == 0:
            raise ValueError("Phone cannot be empty")


@dataclass(frozen=True)
class SearchCriteria:
    """Value object for book search criteria"""
    query: Optional[str] = None
    in_stock_only: bool = False
    
    def has_query(self) -> bool:
        """Check if search has query term"""
        return self.query is not None and len(self.query.strip()) > 0
