from django.db import models


class Shipping(models.Model):
    """
    Shipping model - defines available shipping methods and their fees
    """
    method_name = models.CharField(max_length=100, unique=True)
    fee = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    estimated_days = models.IntegerField(help_text="Estimated delivery days")
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['fee']

    def __str__(self):
        return f"{self.method_name} - ${self.fee}"
