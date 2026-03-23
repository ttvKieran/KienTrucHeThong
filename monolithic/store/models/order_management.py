from django.db import models

# OrderStatus: ID (PK), Name, Description
class OrderStatus(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'order_status'
        verbose_name_plural = 'Order Statuses'


# OrderTimeline: ID (PK), Status, Updated_At, Order_ID (FK)
class OrderTimeline(models.Model):
    id = models.AutoField(primary_key=True)
    status = models.CharField(max_length=100)
    updated_at = models.DateTimeField(auto_now_add=True)
    order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='timeline')

    def __str__(self):
        return f'Order {self.order.id} - {self.status} at {self.updated_at}'

    class Meta:
        db_table = 'order_timeline'
        ordering = ['-updated_at']


# OrderNote: ID (PK), Content, Created_At, Order_ID (FK), Staff_ID (FK)
class OrderNote(models.Model):
    id = models.AutoField(primary_key=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='notes')
    staff = models.ForeignKey('Staff', on_delete=models.CASCADE)

    def __str__(self):
        return f'Note for Order {self.order.id} by {self.staff.name}'

    class Meta:
        db_table = 'order_note'
        ordering = ['-created_at']


# Invoice: ID (PK), Invoice_Date, Total_Amount, Order_ID (FK)
class Invoice(models.Model):
    id = models.AutoField(primary_key=True)
    invoice_date = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    order = models.OneToOneField('Order', on_delete=models.CASCADE, related_name='invoice')

    def __str__(self):
        return f'Invoice {self.id} for Order {self.order.id}'

    class Meta:
        db_table = 'invoice'


# CancelRequest: ID (PK), Reason, Status, Order_ID (FK)
class CancelRequest(models.Model):
    id = models.AutoField(primary_key=True)
    reason = models.TextField()
    status = models.CharField(max_length=50, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='cancel_requests')

    def __str__(self):
        return f'Cancel Request {self.id} for Order {self.order.id}'

    class Meta:
        db_table = 'cancel_request'
