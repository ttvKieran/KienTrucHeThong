from django.db import models


class Order(models.Model):
    """
    Order model - stores customer orders
    """
    customer = models.ForeignKey('store.Customer', on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('processing', 'Processing'),
            ('shipped', 'Shipped'),
            ('delivered', 'Delivered'),
            ('cancelled', 'Cancelled')
        ],
        default='pending'
    )
    shipping = models.ForeignKey('store.Shipping', on_delete=models.SET_NULL, null=True)
    payment = models.ForeignKey('store.Payment', on_delete=models.SET_NULL, null=True)
    shipping_address = models.TextField()
    note = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'store'
        ordering = ['-created_at']

    def __str__(self):
        return f"Order #{self.id} - {self.customer.fullname}"


class OrderItem(models.Model):
    """
    OrderItem model - stores items within an order
    """
    order = models.ForeignKey('store.Order', on_delete=models.CASCADE, related_name='items')
    book = models.ForeignKey('store.Book', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, editable=False)

    class Meta:
        app_label = 'store'

    def save(self, *args, **kwargs):
        self.subtotal = self.quantity * self.price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.book.title} x {self.quantity}"

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
    
    customer = models.ForeignKey('store.Customer', on_delete=models.CASCADE, related_name='orders')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    shipping = models.ForeignKey('store.Shipping', on_delete=models.SET_NULL, null=True)
    payment = models.ForeignKey('store.Payment', on_delete=models.SET_NULL, null=True)
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
    order = models.ForeignKey('store.Order', on_delete=models.CASCADE, related_name='items')
    book = models.ForeignKey('store.Book', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity}x {self.book.title} in Order #{self.order.id}"

    def save(self, *args, **kwargs):
        # Automatically calculate subtotal
        self.subtotal = self.quantity * self.price
        super().save(*args, **kwargs)
