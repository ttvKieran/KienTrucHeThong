from django.db import models
from store.models.customer import Customer

# Category: ID (PK), Name, Description.
class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

# Book: ID (PK), Title, Author, Stock_Quantity (int), Price (double), Category_Id (FK ref Category).
class Book(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    stock_quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
# Rating: ID (PK), Score (double), Book_ID (FK ref Book), Customer_ID (FK ref Customer).
class Rating(models.Model):
    id = models.AutoField(primary_key=True)
    score = models.DecimalField(max_digits=3, decimal_places=2)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE)

    def __str__(self):
        return f'Rating {self.score} for {self.book.title} by {self.customer.name}'