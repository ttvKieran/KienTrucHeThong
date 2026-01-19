"""
Django ORM Models
Framework-specific database models
"""
from django.db import models
from django.contrib.auth.models import User


class BookModel(models.Model):
    """
    Django ORM model for Book
    Infrastructure layer - framework specific
    """
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    stock = models.PositiveIntegerField()
    note = models.TextField(blank=True, null=True)
    slug = models.SlugField(unique=True)

    class Meta:
        db_table = 'books'
        
    def __str__(self):
        return self.title


class CustomerModel(models.Model):
    """
    Django ORM model for Customer
    Infrastructure layer - framework specific
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fullname = models.CharField(max_length=255)
    address = models.TextField()
    phone = models.CharField(max_length=20)
    note = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'customers'
        
    def __str__(self):
        return self.fullname


class CartModel(models.Model):
    """
    Django ORM model for Cart
    Infrastructure layer - framework specific
    """
    customer = models.ForeignKey(CustomerModel, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'carts'
        
    def __str__(self):
        return f"Cart {self.id} for {self.customer.fullname}"


class CartItemModel(models.Model):
    """
    Django ORM model for CartItem
    Infrastructure layer - framework specific
    """
    cart = models.ForeignKey(CartModel, on_delete=models.CASCADE, related_name='items')
    book = models.ForeignKey(BookModel, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'cart_items'
        unique_together = ['cart', 'book']
        
    def __str__(self):
        return f"{self.quantity} of {self.book.title}"
