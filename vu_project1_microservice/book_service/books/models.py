"""
Book Models - Domain entities
"""
from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal


class Book(models.Model):
    """
    Book entity - represents a book in the catalog
    """
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    stock = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)]
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    note = models.TextField(blank=True, null=True)
    slug = models.SlugField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'books'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} by {self.author}"
    
    def is_available(self):
        """Check if book is available in stock"""
        return self.stock > 0
    
    def has_sufficient_stock(self, quantity):
        """Check if book has sufficient stock for requested quantity"""
        return self.stock >= quantity
    
    def reduce_stock(self, quantity):
        """
        Reduce stock by quantity
        Raises ValueError if insufficient stock
        """
        if not self.has_sufficient_stock(quantity):
            raise ValueError(
                f"Insufficient stock. Available: {self.stock}, Requested: {quantity}"
            )
        self.stock -= quantity
        self.save()
    
    def increase_stock(self, quantity):
        """Increase stock by quantity"""
        if quantity < 0:
            raise ValueError("Quantity must be positive")
        self.stock += quantity
        self.save()
