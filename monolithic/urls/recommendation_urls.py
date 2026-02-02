from django.urls import path
from controllers import bookController, aiRecommendationController

urlpatterns = [
    # Basic recommendations (moved to bookController)
    path('by-history/<int:customer_id>/', bookController.recommend_books_by_history, name='recommend_by_history'),
    path('by-rating/', bookController.recommend_books_by_rating, name='recommend_by_rating'),
    path('by-category/', bookController.recommend_books_by_popular_category, name='recommend_by_category'),
    path('similar/<int:book_id>/', bookController.recommend_similar_books, name='recommend_similar'),
    
    # AI-powered recommendations
    path('ai/collaborative/<int:customer_id>/', aiRecommendationController.ai_collaborative_filtering, name='ai_collaborative'),
    path('ai/content-based/<int:customer_id>/', aiRecommendationController.ai_content_based_filtering, name='ai_content_based'),
    path('ai/hybrid/<int:customer_id>/', aiRecommendationController.ai_hybrid_recommendation, name='ai_hybrid'),
    path('ai/trending/', aiRecommendationController.ai_trending_books, name='ai_trending'),
    path('ai/personalized/<int:customer_id>/', aiRecommendationController.ai_personalized_homepage, name='ai_personalized'),
]
