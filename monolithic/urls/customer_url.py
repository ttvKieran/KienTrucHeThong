from django.urls import path
from controllers import customerController

urlpatterns = [
    # Quản lý khách hàng
    path('', customerController.list_customers, name='list_customers'),
    path('<int:customer_id>/', customerController.get_customer, name='get_customer'),
    path('register/', customerController.register_customer, name='register_customer'),
    path('<int:customer_id>/update/', customerController.update_customer, name='update_customer'),
]