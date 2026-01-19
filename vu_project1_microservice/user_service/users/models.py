"""
User Models - Domain entities
"""
from django.db import models
from django.contrib.auth.models import AbstractUser
import re


class User(AbstractUser):
    """
    Custom User model extending Django's AbstractUser
    """
    email = models.EmailField(unique=True)
    
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )
    
    class Meta:
        db_table = 'users'
    
    def __str__(self):
        return self.username


class Customer(models.Model):
    """
    Customer entity - Profile information for users
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='customer_profile'
    )
    fullname = models.CharField(max_length=255)
    address = models.TextField()
    phone = models.CharField(max_length=20)
    note = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'customers'
    
    def __str__(self):
        return f"Customer: {self.fullname}"
    
    def validate(self):
        """Validate customer data"""
        if not self.fullname or len(self.fullname.strip()) == 0:
            raise ValueError("Customer fullname cannot be empty")
        
        if not self.address or len(self.address.strip()) == 0:
            raise ValueError("Customer address cannot be empty")
        
        if not self.phone or len(self.phone.strip()) == 0:
            raise ValueError("Customer phone cannot be empty")
        
        # Basic phone validation
        phone_clean = self.phone.replace('+', '').replace('-', '').replace(' ', '')
        if not phone_clean.isdigit():
            raise ValueError("Invalid phone number format")
    
    def save(self, *args, **kwargs):
        """Override save to validate before saving"""
        self.validate()
        super().save(*args, **kwargs)
