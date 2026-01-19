"""
Cart Service URLs
"""
from django.urls import path
from .views import (
    CartView,
    AddToCartView,
    UpdateCartView,
    RemoveFromCartView,
    CheckoutView,
    OrderListView,
)

urlpatterns = [
    # Cart operations
    path('cart/', CartView.as_view(), name='cart-view'),
    path('cart/add/', AddToCartView.as_view(), name='cart-add'),
    path('cart/update/', UpdateCartView.as_view(), name='cart-update'),
    path('cart/remove/<int:book_id>/', RemoveFromCartView.as_view(), name='cart-remove'),
    path('cart/checkout/', CheckoutView.as_view(), name='cart-checkout'),
    
    # Orders
    path('orders/', OrderListView.as_view(), name='order-list'),
]
