"""
URL Configuration for Framework Layer
"""
from django.urls import path
from framework.views import (
    BookListView,
    BookDetailView,
    CartView,
    AddToCartView,
    UpdateCartItemView,
    RemoveFromCartView,
    RegisterView,
    LoginView,
    ProfileView,
)

urlpatterns = [
    # Book URLs
    path('books', BookListView.as_view(), name='book-list'),
    path('books/<int:book_id>', BookDetailView.as_view(), name='book-detail'),
    
    # Cart URLs
    path('cart', CartView.as_view(), name='cart'),
    path('cart/add', AddToCartView.as_view(), name='cart-add'),
    path('cart/item/<int:book_id>', UpdateCartItemView.as_view(), name='cart-update'),
    path('cart/item/<int:book_id>', RemoveFromCartView.as_view(), name='cart-remove'),
    
    # Auth URLs
    path('auth/register', RegisterView.as_view(), name='auth-register'),
    path('auth/login', LoginView.as_view(), name='auth-login'),
    path('auth/profile', ProfileView.as_view(), name='auth-profile'),
]
