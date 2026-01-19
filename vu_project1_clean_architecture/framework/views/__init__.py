"""
Views package
"""
from .book_views import BookListView, BookDetailView
from .cart_views import CartView, AddToCartView, UpdateCartItemView, RemoveFromCartView
from .auth_views import RegisterView, LoginView, ProfileView

__all__ = [
    'BookListView',
    'BookDetailView',
    'CartView',
    'AddToCartView',
    'UpdateCartItemView',
    'RemoveFromCartView',
    'RegisterView',
    'LoginView',
    'ProfileView',
]
