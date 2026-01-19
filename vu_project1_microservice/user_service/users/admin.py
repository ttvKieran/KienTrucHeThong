from django.contrib import admin
from .models import User, Customer


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'email', 'is_active', 'date_joined']
    list_filter = ['is_active', 'date_joined']
    search_fields = ['username', 'email']


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'fullname', 'phone', 'created_at']
    list_filter = ['created_at']
    search_fields = ['fullname', 'phone', 'user__username']
