from django.contrib import admin

from store.models import (
    Customer, Cart, CartItem, Book,
    Rating, Staff, Order, OrderItem, Shipping, Payment
)

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'fullname', 'address', 'phone')
    search_fields = ('fullname', 'phone')
    
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'created_at', 'is_active')
    search_fields = ('customer__fullname',)
    list_filter = ('is_active', 'created_at')
    
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'cart', 'book', 'quantity', 'price')
    search_fields = ('cart__id', 'book__title')
    
class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'stock', 'slug')
    search_fields = ('title', 'author')
    prepopulated_fields = {'slug': ('title',)}


class RatingAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'book', 'score', 'created_at')
    search_fields = ('customer__fullname', 'book__title')
    list_filter = ('score', 'created_at')
    readonly_fields = ('created_at', 'updated_at')


class StaffAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'role', 'phone', 'hire_date')
    search_fields = ('name', 'phone')
    list_filter = ('role', 'hire_date')
    readonly_fields = ('hire_date',)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('subtotal',)


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'total_price', 'status', 'created_at')
    search_fields = ('customer__fullname', 'id')
    list_filter = ('status', 'created_at')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [OrderItemInline]


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'book', 'quantity', 'price', 'subtotal')
    search_fields = ('order__id', 'book__title')
    readonly_fields = ('subtotal',)


class ShippingAdmin(admin.ModelAdmin):
    list_display = ('id', 'method_name', 'fee', 'estimated_days', 'is_active')
    search_fields = ('method_name',)
    list_filter = ('is_active',)


class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'method_name', 'status', 'transaction_id', 'created_at')
    search_fields = ('method_name', 'transaction_id')
    list_filter = ('status', 'created_at')
    readonly_fields = ('created_at', 'updated_at')
    
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)    
admin.site.register(Book, BookAdmin)
admin.site.register(Rating, RatingAdmin)
admin.site.register(Staff, StaffAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(Shipping, ShippingAdmin)
admin.site.register(Payment, PaymentAdmin)