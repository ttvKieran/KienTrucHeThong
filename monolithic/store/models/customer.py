from django.db import models

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
    
