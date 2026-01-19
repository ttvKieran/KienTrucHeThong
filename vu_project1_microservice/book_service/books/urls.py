"""
Book Service URLs
"""
from django.urls import path
from .views import (
    BookListView,
    BookDetailView,
    BookStockView,
    CheckStockView,
)

urlpatterns = [
    # Book CRUD
    path('books/', BookListView.as_view(), name='book-list'),
    path('books/<int:book_id>/', BookDetailView.as_view(), name='book-detail'),
    
    # Stock management
    path('books/<int:book_id>/stock/', BookStockView.as_view(), name='book-stock'),
    path('books/check-stock/', CheckStockView.as_view(), name='check-stock'),
]
