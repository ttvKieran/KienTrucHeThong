from django.urls import path
from controllers import recommendationController

urlpatterns = [
    # Gợi ý sách
    path('by-history/<int:customer_id>/', recommendationController.recommend_books_by_history, name='recommend_by_history'),
    path('by-rating/', recommendationController.recommend_books_by_rating, name='recommend_by_rating'),
    path('by-category/', recommendationController.recommend_books_by_popular_category, name='recommend_by_category'),
    path('similar/<int:book_id>/', recommendationController.recommend_similar_books, name='recommend_similar'),
]
