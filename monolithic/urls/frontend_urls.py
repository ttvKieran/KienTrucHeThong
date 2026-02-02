from django.urls import path
from django.views.generic import TemplateView

urlpatterns = [
    # Authentication pages
    path('login/', TemplateView.as_view(template_name='auth/login.html'), name='web_login'),
    path('register/', TemplateView.as_view(template_name='auth/register.html'), name='web_register'),
    
    # Book pages
    path('', TemplateView.as_view(template_name='book/list.html'), name='web_home'),
    path('book/<int:book_id>/', TemplateView.as_view(template_name='book/detail.html'), name='web_book_detail'),
    
    # Cart pages
    path('cart/', TemplateView.as_view(template_name='cart/view.html'), name='web_cart'),
    path('checkout/', TemplateView.as_view(template_name='cart/checkout.html'), name='web_checkout'),
    
    # Order pages
    path('orders/', TemplateView.as_view(template_name='order/list.html'), name='web_order_history'),
    path('orders/<int:order_id>/', TemplateView.as_view(template_name='order/detail.html'), name='web_order_detail'),
    
    # Staff pages
    path('staff/dashboard/', TemplateView.as_view(template_name='staff/dashboard.html'), name='web_staff_dashboard'),
    path('staff/orders/', TemplateView.as_view(template_name='staff/orders.html'), name='web_staff_orders'),
    
    # Recommendations page
    path('recommendations/', TemplateView.as_view(template_name='recommendation/list.html'), name='web_recommendations'),
    
    # AI Recommendations page
    path('ai-recommendations/', TemplateView.as_view(template_name='recommendation/ai.html'), name='web_ai_recommendations'),
]
