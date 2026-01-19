from django.urls import path, include
from .views import page_views

urlpatterns = [
    # Frontend pages
    path("", page_views.home, name="home"),
    path("login", page_views.login_page, name="login"),
    path("register", page_views.register_page, name="register"),
    path("books", page_views.books_page, name="books"),
    path("cart", page_views.cart_page, name="cart"),
    path("checkout", page_views.checkout_page, name="checkout"),
    path("orders", page_views.orders_page, name="orders"),
    path("recommendations/", page_views.recommendations_page, name="recommendations"),
    path("profile", page_views.profile_page, name="profile"),
    
    # API endpoints - organized by module
    path("api/auth/", include('bookstore.urls_module.auth_urls')),
    path("api/books/", include('bookstore.urls_module.book_urls')),
    path("api/cart/", include('bookstore.urls_module.cart_urls')),
    path("api/orders/", include('bookstore.urls_module.order_urls')),
    path("api/ratings/", include('bookstore.urls_module.rating_urls')),
    path("api/recommendations/", include('bookstore.urls_module.recommendation_urls')),
]