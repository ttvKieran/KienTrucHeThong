from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Rating(models.Model):
    """
    Rating model - stores customer ratings for books
    """
    customer = models.ForeignKey('store.Customer', on_delete=models.CASCADE, related_name='ratings')
    book = models.ForeignKey('store.Book', on_delete=models.CASCADE, related_name='ratings')
    score = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Rating score from 1 to 5"
    )
    review = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['customer', 'book']
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.customer.fullname} rated {self.book.title}: {self.score}/5"
