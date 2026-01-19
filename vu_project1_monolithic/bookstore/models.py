# Import all models from models_module for backward compatibility
from .models_module import Customer, Book, Cart, CartItem

__all__ = ['Customer', 'Book', 'Cart', 'CartItem']
