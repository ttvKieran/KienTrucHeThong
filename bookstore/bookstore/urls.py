"""
URL configuration for bookstore project.
"""
from django.contrib import admin
from django.urls import path, include
from store.controllers import page_views

urlpatterns = [
    path("admin/", admin.site.urls),
    
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
    
    # API endpoints
    path("api/auth/", include('store.urls.customer_urls')),
    path("api/books/", include('store.urls.book_urls')),
    path("api/cart/", include('store.urls.cart_urls')),
    path("api/orders/", include('store.urls.order_urls')),
    path("api/ratings/", include('store.urls.rating_urls')),
    path("api/recommendations/", include('store.urls.recommendation_urls')),
]
