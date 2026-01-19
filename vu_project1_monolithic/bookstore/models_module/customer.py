from django.db import models


class Customer(models.Model):
    """
    Customer model extends Django's User model with additional attributes
    """
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    fullname = models.CharField(max_length=255)
    address = models.TextField()
    phone = models.CharField(max_length=20)
    note = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.fullname
