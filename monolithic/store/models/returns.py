from django.db import models

# ReturnRequest: ID (PK), Reason, Status
class ReturnRequest(models.Model):
    id = models.AutoField(primary_key=True)
    reason = models.TextField()
    status = models.CharField(max_length=50, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='return_requests')
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f'Return Request {self.id} - {self.status}'

    class Meta:
        db_table = 'return_request'


# Reservation: ID (PK), Quantity, Condition, Book_ID (FK), Return_Request_ID (FK)
class Reservation(models.Model):
    id = models.AutoField(primary_key=True)
    quantity = models.IntegerField()
    condition = models.CharField(max_length=100)
    book = models.ForeignKey('Book', on_delete=models.CASCADE)
    return_request = models.ForeignKey(ReturnRequest, on_delete=models.CASCADE, related_name='reservations')

    def __str__(self):
        return f'Reservation {self.id} - {self.book.title}'

    class Meta:
        db_table = 'reservation'
