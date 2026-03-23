from django.db import models

# Review: ID (PK), Rating, Comment, Customer_ID (FK), Book_ID (FK)
class Review(models.Model):
    id = models.AutoField(primary_key=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2)
    comment = models.TextField(blank=True, null=True)
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE)
    book = models.ForeignKey('Book', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Review {self.rating} for {self.book.title} by {self.customer.name}'

    class Meta:
        db_table = 'review'
