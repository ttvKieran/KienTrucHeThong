from django.contrib import admin
from store.models import *

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'author', 'price', 'stock_quantity', 'category']
    search_fields = ['title', 'author']
    list_filter = ['category']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description']
    search_fields = ['name']

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ['id', 'book', 'customer', 'score']
    list_filter = ['score']
    search_fields = ['book__title', 'customer__name']

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'email', 'address']
    search_fields = ['name', 'email']

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['id', 'house_number', 'building', 'street', 'province']
    search_fields = ['street', 'province']

@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'role']
    list_filter = ['role']
    search_fields = ['name']

@admin.register(Shipping)
class ShippingAdmin(admin.ModelAdmin):
    list_display = ['id', 'method_name', 'fee']
    search_fields = ['method_name']

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['id', 'method_name', 'status']
    list_filter = ['status']
    search_fields = ['method_name']

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'is_active']
    list_filter = ['is_active']
    search_fields = ['customer__name']

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'cart', 'book', 'quantity']
    search_fields = ['book__title', 'cart__customer__name']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'staff', 'total_price', 'status', 'order_date']
    list_filter = ['status', 'order_date']
    search_fields = ['customer__name', 'staff__name']
    date_hierarchy = 'order_date'

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'book', 'quantity']
    search_fields = ['book__title', 'order__customer__name']