from django.urls import path
from controllers import customerController

urlpatterns = [
    # Authentication API
    path('login/', customerController.login_api, name='login_api'),
    path('logout/', customerController.logout_api, name='logout_api'),
    
    # Quản lý khách hàng
    path('', customerController.list_customers, name='list_customers'),
    path('<int:customer_id>/', customerController.get_customer, name='get_customer'),
    path('register/', customerController.register_customer, name='register_customer'),
    path('<int:customer_id>/update/', customerController.update_customer, name='update_customer'),
]