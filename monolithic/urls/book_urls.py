from django.urls import path
from controllers import bookController

urlpatterns = [
    # Xem và tìm kiếm sách
    path('', bookController.list_books, name='list_books'),
    path('search/', bookController.search_books, name='search_books'),
    path('categories/', bookController.list_categories, name='list_categories'),
    path('<int:book_id>/', bookController.get_book, name='get_book'),
    
    # Rating
    path('<int:book_id>/ratings/', bookController.get_book_ratings, name='get_book_ratings'),
    path('<int:book_id>/rating/add/', bookController.add_rating, name='add_rating'),
]