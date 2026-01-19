from django.contrib import admin
from .models import Book


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'author', 'stock', 'price', 'created_at']
    list_filter = ['created_at', 'author']
    search_fields = ['title', 'author']
    ordering = ['-created_at']
