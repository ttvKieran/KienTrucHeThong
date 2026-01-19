from rest_framework import serializers
from ..models import Book


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('id', 'title', 'author', 'stock', 'note', 'slug')
        read_only_fields = ('slug',)
