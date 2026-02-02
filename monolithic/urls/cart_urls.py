from django.urls import path
from controllers import customerController

urlpatterns = [
    # Quản lý giỏ hàng (moved to customerController)
    path('<int:customer_id>/', customerController.get_cart, name='get_cart'),
    path('<int:customer_id>/create/', customerController.create_cart, name='create_cart'),
    path('<int:customer_id>/clear/', customerController.clear_cart, name='clear_cart'),
    path('add/', customerController.add_to_cart, name='add_to_cart'),
    
    # Quản lý cart items
    path('update/', customerController.update_cart_item, name='update_cart_item'),
    path('remove/', customerController.remove_from_cart, name='remove_from_cart'),
]
