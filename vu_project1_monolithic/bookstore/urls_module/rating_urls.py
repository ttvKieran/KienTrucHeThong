from django.urls import path, include
from rest_framework.routers import DefaultRouter
from ..views.rating_views import RatingViewSet

router = DefaultRouter()  # Keep default trailing_slash=True
router.register(r'', RatingViewSet, basename='rating')

urlpatterns = [
    path('', include(router.urls)),
]
