from django.db import models

# Cart: ID (PK), Is_Active (boolean/bit), Customer_ID (FK ref Customer).
class Cart(models.Model):
    id = models.AutoField(primary_key=True)
    is_active = models.BooleanField(default=True)
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE)

    def __str__(self):
        return f"Cart {self.id} for Customer {self.customer.id}"
    
# CartItem: ID (PK), Quantity (int), Cart_ID (FK ref Cart), Book_ID (FK ref Book).
class CartItem(models.Model):
    id = models.AutoField(primary_key=True)
    quantity = models.IntegerField()
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    book = models.ForeignKey('Book', on_delete=models.CASCADE)

    def __str__(self):
        return f"CartItem {self.id} (Quantity: {self.quantity}) in Cart {self.cart.id} for Book {self.book.id}"
    
# Shipping: ID (PK), Method_Name, Fee (double).
class Shipping(models.Model):
    id = models.AutoField(primary_key=True)
    method_name = models.CharField(max_length=255)
    fee = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Shipping {self.method_name} (Fee: {self.fee})"
    
# Payment: ID (PK), Method_Name, Status.
class Payment(models.Model):
    id = models.AutoField(primary_key=True)
    method_name = models.CharField(max_length=255)
    status = models.CharField(max_length=50)

    def __str__(self):
        return f"Payment {self.method_name} (Status: {self.status})"
    
# Order: ID (PK), Total_Price (double), Order_Date (Date), Status, Customer_ID (FK), Staff_ID (FK), Shipping_ID (FK), Payment_ID (FK).
class Order(models.Model):
    id = models.AutoField(primary_key=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    order_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=50)
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE)
    staff = models.ForeignKey('Staff', on_delete=models.CASCADE)
    shipping = models.ForeignKey(Shipping, on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE)

    def __str__(self):
        return f"Order {self.id} (Total Price: {self.total_price}, Status: {self.status})"

# OrderItem: ID (PK), Quantity (int), Order_ID (FK ref Order), Book_ID (FK ref Book).
class OrderItem(models.Model):
    id = models.AutoField(primary_key=True)
    quantity = models.IntegerField()
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    book = models.ForeignKey('Book', on_delete=models.CASCADE)

    def __str__(self):
        return f"OrderItem {self.id} (Quantity: {self.quantity}) in Order {self.order.id} for Book {self.book.id}"    