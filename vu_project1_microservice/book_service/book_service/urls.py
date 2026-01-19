"""
Book Service URL Configuration
"""
from django.contrib import admin
from django.urls import path, include
from books.views import health_check

urlpatterns = [
    path('admin/', admin.site.urls),
    path('health/', health_check, name='health'),
    path('api/', include('books.urls')),
]
