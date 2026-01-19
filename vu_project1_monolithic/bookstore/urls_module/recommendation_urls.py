from django.urls import path
from ..views import recommendation_views

urlpatterns = [
    path('recommendations/', recommendation_views.get_recommendations, name='api-recommendations'),
    path('trending/', recommendation_views.get_trending_books, name='api-trending-books'),
    path('similar/<int:book_id>/', recommendation_views.get_similar_books, name='api-similar-books'),
    path('highly-rated/', recommendation_views.get_highly_rated_books, name='api-highly-rated-books'),
]
