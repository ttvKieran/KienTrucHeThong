from django.urls import path
from store.controllers.orderController import order_views

urlpatterns = [
    # Orders
    path('', order_views.order_list_create, name='order-list-create'),
    path('<int:order_id>/', order_views.order_detail, name='order-detail'),
    path('<int:order_id>/cancel/', order_views.cancel_order, name='order-cancel'),
    path('<int:order_id>/update_status/', order_views.update_order_status, name='order-update-status'),
    
    # Shipping
    path('shipping/', order_views.shipping_list, name='shipping-list'),
]
