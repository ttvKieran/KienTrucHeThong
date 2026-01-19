from django.db import models


class Book(models.Model):
    """
    Book model for catalog management
    """
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    stock = models.PositiveIntegerField()
    note = models.TextField(blank=True, null=True)
    slug = models.SlugField(unique=True)

    class Meta:
        app_label = 'store'

    def __str__(self):
        return self.title
