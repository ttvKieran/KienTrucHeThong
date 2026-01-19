from django.contrib import admin

from .models import Customer, Cart, CartItem, Book

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'fullname', 'address', 'phone')
    search_fields = ('fullname', 'phone')
    
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'created_at')
    search_fields = ('customer__fullname',)
    
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'cart', 'book', 'quantity', 'price')
    search_fields = ('cart__id', 'book__title')
    
class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'stock', 'slug')
    search_fields = ('title', 'author')
    prepopulated_fields = {'slug': ('title',)}
    
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)    
admin.site.register(Book, BookAdmin)