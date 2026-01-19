"""
Book Serializers
"""
from rest_framework import serializers
from .models import Book


class BookSerializer(serializers.ModelSerializer):
    """Serializer for Book model"""
    
    class Meta:
        model = Book
        fields = [
            'id', 'title', 'author', 'stock', 'price',
            'note', 'slug', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate_title(self, value):
        """Validate title is not empty"""
        if not value or len(value.strip()) == 0:
            raise serializers.ValidationError("Book title cannot be empty")
        return value
    
    def validate_author(self, value):
        """Validate author is not empty"""
        if not value or len(value.strip()) == 0:
            raise serializers.ValidationError("Book author cannot be empty")
        return value
    
    def validate_stock(self, value):
        """Validate stock is not negative"""
        if value < 0:
            raise serializers.ValidationError("Stock cannot be negative")
        return value
    
    def validate_price(self, value):
        """Validate price is not negative"""
        if value < 0:
            raise serializers.ValidationError("Price cannot be negative")
        return value


class BookListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for book list"""
    
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'stock', 'price']


class StockUpdateSerializer(serializers.Serializer):
    """Serializer for stock updates"""
    quantity = serializers.IntegerField(min_value=1)
    operation = serializers.ChoiceField(choices=['increase', 'decrease'])
