from django.db import models
from .customer import Customer
from .book import Book
from .shipping import Shipping
from .payment import Payment


class Order(models.Model):
    """
    Order model - stores customer orders
    """
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    shipping = models.ForeignKey(Shipping, on_delete=models.SET_NULL, null=True)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, null=True)
    shipping_address = models.TextField()
    note = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Order #{self.id} - {self.customer.fullname} - ${self.total_price}"


class OrderItem(models.Model):
    """
    OrderItem model - stores individual items within an order
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity}x {self.book.title} in Order #{self.order.id}"

    def save(self, *args, **kwargs):
        # Automatically calculate subtotal
        self.subtotal = self.quantity * self.price
        super().save(*args, **kwargs)
