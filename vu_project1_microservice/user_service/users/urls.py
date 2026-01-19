"""
User Service URLs
"""
from django.urls import path
from .views import (
    RegisterView,
    LoginView,
    ProfileView,
    UserDetailView,
)

urlpatterns = [
    # Authentication
    path('users/register/', RegisterView.as_view(), name='register'),
    path('users/login/', LoginView.as_view(), name='login'),
    
    # Profile
    path('users/profile/', ProfileView.as_view(), name='profile'),
    
    # User details (for inter-service communication)
    path('users/<int:user_id>/', UserDetailView.as_view(), name='user-detail'),
]
