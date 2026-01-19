from django.db import models
from django.contrib.auth.models import User


class Staff(models.Model):
    """
    Staff model - extends auth.User with staff-specific information
    """
    ROLE_CHOICES = [
        ('manager', 'Manager'),
        ('sales', 'Sales Staff'),
        ('warehouse', 'Warehouse Staff'),
        ('customer_service', 'Customer Service'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='staff_profile')
    name = models.CharField(max_length=255)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)
    phone = models.CharField(max_length=20, blank=True, null=True)
    hire_date = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Staff"

    def __str__(self):
        return f"{self.name} - {self.get_role_display()}"
