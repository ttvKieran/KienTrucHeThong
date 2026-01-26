from django.urls import path
from controllers import cartController

urlpatterns = [
    # Quản lý giỏ hàng
    path('<int:customer_id>/', cartController.get_cart, name='get_cart'),
    path('<int:customer_id>/create/', cartController.create_cart, name='create_cart'),
    path('<int:customer_id>/add/', cartController.add_to_cart, name='add_to_cart'),
    path('<int:customer_id>/clear/', cartController.clear_cart, name='clear_cart'),
    
    # Quản lý cart items
    path('items/<int:cart_item_id>/update/', cartController.update_cart_item, name='update_cart_item'),
    path('items/<int:cart_item_id>/remove/', cartController.remove_from_cart, name='remove_from_cart'),
]
