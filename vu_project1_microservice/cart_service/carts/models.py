"""
Cart Models - Domain entities
"""
from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal


class Cart(models.Model):
    """
    Cart entity - represents a shopping cart
    """
    user_id = models.IntegerField()  # Reference to User in User Service
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'carts'
    
    def __str__(self):
        return f"Cart for user {self.user_id}"
    
    def get_total(self):
        """Calculate total cart value"""
        return sum(item.get_subtotal() for item in self.items.all())
    
    def get_item_count(self):
        """Get total number of items in cart"""
        return sum(item.quantity for item in self.items.all())


class CartItem(models.Model):
    """
    CartItem entity - represents items in cart
    """
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='items'
    )
    book_id = models.IntegerField()  # Reference to Book in Book Service
    book_title = models.CharField(max_length=255)
    quantity = models.IntegerField(
        validators=[MinValueValidator(1)]
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'cart_items'
        unique_together = ['cart', 'book_id']
    
    def __str__(self):
        return f"{self.book_title} x{self.quantity}"
    
    def get_subtotal(self):
        """Calculate subtotal for this item"""
        return self.price * self.quantity


class Order(models.Model):
    """
    Order entity - represents a completed order
    """
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    user_id = models.IntegerField()  # Reference to User in User Service
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'orders'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Order #{self.id} - {self.status}"


class OrderItem(models.Model):
    """
    OrderItem entity - represents items in an order
    """
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items'
    )
    book_id = models.IntegerField()
    book_title = models.CharField(max_length=255)
    quantity = models.IntegerField(
        validators=[MinValueValidator(1)]
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    subtotal = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    
    class Meta:
        db_table = 'order_items'
    
    def __str__(self):
        return f"{self.book_title} x{self.quantity}"
