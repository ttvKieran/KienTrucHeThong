"""
Gateway URL routing
"""
from django.urls import path
from .views import (
    UserServiceProxy,
    BookServiceProxy,
    CartServiceProxy,
)

urlpatterns = [
    # User Service routes
    path('users/register/', UserServiceProxy.as_view(), name='user-register'),
    path('users/login/', UserServiceProxy.as_view(), name='user-login'),
    path('users/profile/', UserServiceProxy.as_view(), name='user-profile'),
    
    # Book Service routes
    path('books/', BookServiceProxy.as_view(), name='book-list'),
    path('books/<int:book_id>/', BookServiceProxy.as_view(), name='book-detail'),
    
    # Cart Service routes
    path('cart/', CartServiceProxy.as_view(), name='cart-view'),
    path('cart/add/', CartServiceProxy.as_view(), name='cart-add'),
    path('cart/update/', CartServiceProxy.as_view(), name='cart-update'),
    path('cart/remove/<int:book_id>/', CartServiceProxy.as_view(), name='cart-remove'),
    path('cart/checkout/', CartServiceProxy.as_view(), name='cart-checkout'),
]
