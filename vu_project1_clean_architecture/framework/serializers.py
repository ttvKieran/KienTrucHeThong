"""
Serializers for converting domain entities to JSON
Framework layer - adapters for HTTP responses
"""
from rest_framework import serializers


class BookSerializer(serializers.Serializer):
    """Serializer for Book entity"""
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField()
    author = serializers.CharField()
    stock = serializers.IntegerField()
    note = serializers.CharField(allow_blank=True, allow_null=True)
    slug = serializers.SlugField()
    is_available = serializers.SerializerMethodField()
    
    def get_is_available(self, obj):
        """Check if book is available"""
        return obj.is_available()


class CartItemSerializer(serializers.Serializer):
    """Serializer for CartItem entity"""
    id = serializers.IntegerField(read_only=True)
    book_id = serializers.IntegerField()
    book_title = serializers.CharField()
    quantity = serializers.IntegerField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    subtotal = serializers.SerializerMethodField()
    
    def get_subtotal(self, obj):
        """Calculate subtotal"""
        return obj.get_subtotal()


class CartSerializer(serializers.Serializer):
    """Serializer for Cart entity"""
    id = serializers.IntegerField(read_only=True)
    customer_id = serializers.IntegerField()
    items = CartItemSerializer(many=True)
    total = serializers.SerializerMethodField()
    total_items = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(read_only=True)
    
    def get_total(self, obj):
        """Calculate total"""
        return obj.get_total()
    
    def get_total_items(self, obj):
        """Get total items count"""
        return obj.get_total_items()


class CustomerSerializer(serializers.Serializer):
    """Serializer for Customer entity"""
    id = serializers.IntegerField(read_only=True)
    user_id = serializers.IntegerField()
    fullname = serializers.CharField()
    address = serializers.CharField()
    phone = serializers.CharField()
    note = serializers.CharField(allow_blank=True, allow_null=True)
