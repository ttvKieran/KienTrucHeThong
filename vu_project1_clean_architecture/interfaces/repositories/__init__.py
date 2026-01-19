"""
Repository Interfaces
"""
from .book_repository import IBookRepository
from .customer_repository import ICustomerRepository
from .cart_repository import ICartRepository
from .auth_repository import IAuthRepository

__all__ = [
    'IBookRepository',
    'ICustomerRepository',
    'ICartRepository',
    'IAuthRepository',
]
