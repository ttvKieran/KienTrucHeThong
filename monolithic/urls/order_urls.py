from django.urls import path
from controllers import orderController

urlpatterns = [
    # Quản lý đơn hàng
    path('', orderController.list_orders, name='list_orders'),
    path('<int:order_id>/', orderController.get_order, name='get_order'),
    path('customer/<int:customer_id>/', orderController.get_customer_orders, name='get_customer_orders'),
    
    # Tạo đơn hàng
    path('create/<int:customer_id>/', orderController.create_order_from_cart, name='create_order_from_cart'),
    path('<int:order_id>/status/', orderController.update_order_status, name='update_order_status'),
    
    # Phương thức shipping và payment
    path('shipping-methods/', orderController.list_shipping_methods, name='list_shipping_methods'),
    path('payment-methods/', orderController.list_payment_methods, name='list_payment_methods'),
    path('shipping-methods/create/', orderController.create_shipping_method, name='create_shipping_method'),
    path('payment-methods/create/', orderController.create_payment_method, name='create_payment_method'),
]