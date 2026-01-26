from django.urls import path
from controllers import frontendController

urlpatterns = [
    # Authentication
    path('login/', frontendController.login_view, name='web_login'),
    path('register/', frontendController.register_view, name='web_register'),
    path('logout/', frontendController.logout_view, name='web_logout'),
    
    # Book views
    path('', frontendController.book_list, name='web_home'),
    path('books/<int:book_id>/', frontendController.book_detail, name='web_book_detail'),
    
    # Cart views
    path('cart/', frontendController.cart_view, name='web_cart'),
    path('cart/add/<int:book_id>/', frontendController.add_to_cart, name='web_add_to_cart'),
    path('cart/update/<int:item_id>/', frontendController.update_cart_item, name='web_update_cart_item'),
    path('cart/remove/<int:item_id>/', frontendController.remove_from_cart, name='web_remove_from_cart'),
    
    # Checkout & Orders
    path('checkout/', frontendController.checkout, name='web_checkout'),
    path('order/place/', frontendController.place_order, name='web_place_order'),
    path('orders/', frontendController.order_history, name='web_order_history'),
    path('orders/<int:order_id>/', frontendController.order_detail, name='web_order_detail'),
    
    # Staff management
    path('staff/dashboard/', frontendController.staff_dashboard, name='web_staff_dashboard'),
    path('staff/book/add/', frontendController.staff_add_book, name='web_staff_add_book'),
    path('staff/book/<int:book_id>/update-stock/', frontendController.staff_update_stock, name='web_staff_update_stock'),
    path('staff/book/<int:book_id>/delete/', frontendController.staff_delete_book, name='web_staff_delete_book'),
    
    # Recommendations
    path('recommendations/', frontendController.recommendation_list, name='web_recommendations'),
]
