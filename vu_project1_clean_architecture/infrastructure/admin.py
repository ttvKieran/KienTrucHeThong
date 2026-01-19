"""
Django Admin Configuration
Infrastructure layer - Admin interface for models
"""
from django.contrib import admin
from .models import CustomerModel, CartModel, CartItemModel, BookModel


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'fullname', 'address', 'phone', 'user')
    search_fields = ('fullname', 'phone', 'user__username')
    list_filter = ('user',)


class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'created_at')
    search_fields = ('customer__fullname',)
    list_filter = ('created_at',)
    date_hierarchy = 'created_at'


class CartItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'cart', 'book', 'quantity', 'price', 'get_subtotal')
    search_fields = ('cart__id', 'book__title')
    list_filter = ('cart', 'book')
    
    def get_subtotal(self, obj):
        return obj.quantity * obj.price
    get_subtotal.short_description = 'Subtotal'


class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'stock', 'slug')
    search_fields = ('title', 'author')
    list_filter = ('author',)
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('title',)


admin.site.register(CustomerModel, CustomerAdmin)
admin.site.register(CartModel, CartAdmin)
admin.site.register(CartItemModel, CartItemAdmin)    
admin.site.register(BookModel, BookAdmin)

# Customize admin site header
admin.site.site_header = "Bookstore Clean Architecture Admin"
admin.site.site_title = "Bookstore Admin"
admin.site.index_title = "Welcome to Bookstore Management"
