from django.db import models

# PaymentMethod: ID (PK), Name, Code, Is_Active
class PaymentMethod(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'payment_method'


# PaymentStatus: ID (PK), Code, Description
class PaymentStatus(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.code

    class Meta:
        db_table = 'payment_status'
        verbose_name_plural = 'Payment Statuses'


# Payment: ID (PK), Total_Amount, Status, Created_At, Order_ID (FK)
# Note: Updated to avoid conflict with existing Payment model in order.py
class PaymentTransaction(models.Model):
    id = models.AutoField(primary_key=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='payment_transactions')

    def __str__(self):
        return f'Payment {self.id} for Order {self.order.id}'

    class Meta:
        db_table = 'payment_transaction'


# Transaction: ID (PK), Amount, Status, Transaction_Code, Transaction_Date, Error_Message, Payment_ID (FK), Payment_Method_ID (FK)
class Transaction(models.Model):
    id = models.AutoField(primary_key=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50)
    transaction_code = models.CharField(max_length=100, unique=True)
    transaction_date = models.DateTimeField(auto_now_add=True)
    error_message = models.TextField(blank=True, null=True)
    payment = models.ForeignKey('Payment', on_delete=models.CASCADE, related_name='transactions')
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE)

    def __str__(self):
        return f'Transaction {self.transaction_code} - {self.status}'

    class Meta:
        db_table = 'transaction'


# PaymentLog: ID (PK), Action, Created_At, Payment_ID (FK)
class PaymentLog(models.Model):
    id = models.AutoField(primary_key=True)
    action = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    payment = models.ForeignKey('Payment', on_delete=models.CASCADE, related_name='logs')

    def __str__(self):
        return f'Log {self.id} - {self.action}'

    class Meta:
        db_table = 'payment_log'
        ordering = ['-created_at']


# PaymentFee: ID (PK), Fee_Type, Amount, Payment_ID (FK)
class PaymentFee(models.Model):
    id = models.AutoField(primary_key=True)
    fee_type = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment = models.ForeignKey('Payment', on_delete=models.CASCADE, related_name='fees')

    def __str__(self):
        return f'{self.fee_type} - {self.amount}'

    class Meta:
        db_table = 'payment_fee'


# PaymentAttempt: ID (PK), Attempt_Time, Result, Payment_ID (FK)
class PaymentAttempt(models.Model):
    id = models.AutoField(primary_key=True)
    attempt_time = models.DateTimeField(auto_now_add=True)
    result = models.CharField(max_length=50)
    payment = models.ForeignKey('Payment', on_delete=models.CASCADE, related_name='attempts')

    def __str__(self):
        return f'Attempt {self.id} - {self.result} at {self.attempt_time}'

    class Meta:
        db_table = 'payment_attempt'


# Refund: ID (PK), Amount, Reason, Status, Payment_ID (FK)
class Refund(models.Model):
    id = models.AutoField(primary_key=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    reason = models.TextField()
    status = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    payment = models.ForeignKey('Payment', on_delete=models.CASCADE, related_name='refunds')

    def __str__(self):
        return f'Refund {self.id} - {self.amount} ({self.status})'

    class Meta:
        db_table = 'refund'
