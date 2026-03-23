from django.db import models

from monolithic.store.models.book import Category

# Address: ID (PK), House_Number, Building, Street, Province.
class Address(models.Model):
    id = models.AutoField(primary_key=True)
    house_number = models.CharField(max_length=10)
    building = models.CharField(max_length=100, blank=True, null=True)
    street = models.CharField(max_length=100)
    province = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.house_number} {self.building}, {self.street}, {self.province}"
    
# Customer: ID (PK), Name, Email, Password, Address_Id (FK ref Address).
class Customer(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
# MembershipTier: Bronze, Silver, Gold, Platinum
class MembershipTier(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    priority = models.IntegerField()  # For tier hierarchy

# CustomerMembership: Many-to-many relationship
class CustomerMembership(models.Model):
    customer = models.ForeignKey(Customer)
    tier = models.ForeignKey(MembershipTier)
    joined_date = models.DateField()
    is_active = models.BooleanField()

# DiscountPolicy: Time-based discount rules
class DiscountPolicy(models.Model):
    tier = models.ForeignKey(MembershipTier)
    discount_percentage = models.DecimalField()
    valid_from = models.DateField()
    valid_to = models.DateField()
    min_order_value = models.DecimalField()
    applicable_categories = models.ManyToManyField(Category)