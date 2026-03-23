from django.db import models

# ShippingMethod: ID (PK), Name, Base_Fee
class ShippingMethod(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    base_fee = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'shipping_method'


# ShipmentStatus: ID (PK), Code, Description
class ShipmentStatus(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.code

    class Meta:
        db_table = 'shipment_status'
        verbose_name_plural = 'Shipment Statuses'


# Carrier: ID (PK), Name, Hotline
class Carrier(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    hotline = models.CharField(max_length=20)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'carrier'


# Shipment: ID (PK), Tracking_Number, Status, Actual_Fee, Created_At, Delivery_Date, Order_ID (FK), Method_ID (FK)
class Shipment(models.Model):
    id = models.AutoField(primary_key=True)
    tracking_number = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=50)
    actual_fee = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    delivery_date = models.DateTimeField(blank=True, null=True)
    order = models.OneToOneField('Order', on_delete=models.CASCADE, related_name='shipment')
    method = models.ForeignKey(ShippingMethod, on_delete=models.CASCADE)
    carrier = models.ForeignKey(Carrier, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f'Shipment {self.tracking_number}'

    class Meta:
        db_table = 'shipment'


# ShipmentHistory: ID (PK), Status, Location, Description, Shipment_ID (FK)
class ShipmentHistory(models.Model):
    id = models.AutoField(primary_key=True)
    status = models.CharField(max_length=50)
    location = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    shipment = models.ForeignKey(Shipment, on_delete=models.CASCADE, related_name='history')

    def __str__(self):
        return f'{self.shipment.tracking_number} - {self.status} at {self.location}'

    class Meta:
        db_table = 'shipment_history'
        verbose_name_plural = 'Shipment Histories'
        ordering = ['-created_at']


# DeliveryAttempt: ID (PK), Attempt_Time, Result, Shipment_ID (FK)
class DeliveryAttempt(models.Model):
    id = models.AutoField(primary_key=True)
    attempt_time = models.DateTimeField(auto_now_add=True)
    result = models.CharField(max_length=50)
    note = models.TextField(blank=True, null=True)
    shipment = models.ForeignKey(Shipment, on_delete=models.CASCADE, related_name='delivery_attempts')

    def __str__(self):
        return f'Delivery Attempt {self.id} - {self.result}'

    class Meta:
        db_table = 'delivery_attempt'


# ShipmentPackage: ID (PK), Weight, Length, Width, Height, Shipment_ID (FK)
class ShipmentPackage(models.Model):
    id = models.AutoField(primary_key=True)
    weight = models.DecimalField(max_digits=8, decimal_places=2)  # kg
    length = models.DecimalField(max_digits=8, decimal_places=2)  # cm
    width = models.DecimalField(max_digits=8, decimal_places=2)   # cm
    height = models.DecimalField(max_digits=8, decimal_places=2)  # cm
    shipment = models.OneToOneField(Shipment, on_delete=models.CASCADE, related_name='package')

    def __str__(self):
        return f'Package for {self.shipment.tracking_number}'

    class Meta:
        db_table = 'shipment_package'
