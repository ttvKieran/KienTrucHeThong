from django.db import models

# Author: ID (PK), Name, Bio
class Author(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'author'


# BookAuthor: ID (PK), Book_ID (FK), Author_ID (FK)
class BookAuthor(models.Model):
    id = models.AutoField(primary_key=True)
    book = models.ForeignKey('Book', on_delete=models.CASCADE, related_name='book_authors')
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='book_authors')

    def __str__(self):
        return f'{self.book.title} by {self.author.name}'

    class Meta:
        db_table = 'book_author'
        unique_together = ('book', 'author')
