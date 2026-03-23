from django.db import models

# Promotion: ID (PK), Name, Start_Date, End_Date, Discount_Percent
class Promotion(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    discount_percent = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'promotion'


# Voucher: ID (PK), Code, Discount_Amount, Min_Order_Value, Expiry_Date
class Voucher(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=50, unique=True)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2)
    min_order_value = models.DecimalField(max_digits=10, decimal_places=2)
    expiry_date = models.DateField()
    is_active = models.BooleanField(default=True)
    usage_count = models.IntegerField(default=0)
    max_usage = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.code

    class Meta:
        db_table = 'voucher'
