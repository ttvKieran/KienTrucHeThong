from django.db import models


class Cart(models.Model):
    """
    Shopping cart model
    """
    customer = models.ForeignKey('store.Customer', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        app_label = 'store'

    def __str__(self):
        return f"Cart {self.id} for {self.customer.fullname}"


class CartItem(models.Model):
    """
    Cart item model - represents items in shopping cart
    """
    cart = models.ForeignKey('store.Cart', on_delete=models.CASCADE)
    book = models.ForeignKey('store.Book', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        app_label = 'store'

    def __str__(self):
        return f"{self.quantity} of {self.book.title} in Cart {self.cart.id}"
