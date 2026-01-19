from django.db import models
from .customer import Customer
from .book import Book


class Cart(models.Model):
    """
    Shopping cart model
    """
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Cart {self.id} for {self.customer.fullname}"


class CartItem(models.Model):
    """
    Cart item model - represents items in shopping cart
    """
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} of {self.book.title} in Cart {self.cart.id}"
