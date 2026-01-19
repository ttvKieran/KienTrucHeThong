"""
Cart Serializers
"""
from rest_framework import serializers
from .models import Cart, CartItem, Order, OrderItem


class CartItemSerializer(serializers.ModelSerializer):
    """Serializer for CartItem model"""
    subtotal = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        read_only=True,
        source='get_subtotal'
    )
    
    class Meta:
        model = CartItem
        fields = ['id', 'book_id', 'book_title', 'quantity', 'price', 'subtotal']
        read_only_fields = ['id']


class CartSerializer(serializers.ModelSerializer):
    """Serializer for Cart model"""
    items = CartItemSerializer(many=True, read_only=True)
    total = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        read_only=True,
        source='get_total'
    )
    item_count = serializers.IntegerField(
        read_only=True,
        source='get_item_count'
    )
    
    class Meta:
        model = Cart
        fields = ['id', 'user_id', 'items', 'total', 'item_count', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class AddToCartSerializer(serializers.Serializer):
    """Serializer for adding items to cart"""
    book_id = serializers.IntegerField(min_value=1)
    quantity = serializers.IntegerField(min_value=1)


class UpdateCartItemSerializer(serializers.Serializer):
    """Serializer for updating cart item quantity"""
    book_id = serializers.IntegerField(min_value=1)
    quantity = serializers.IntegerField(min_value=1)


class OrderItemSerializer(serializers.ModelSerializer):
    """Serializer for OrderItem model"""
    
    class Meta:
        model = OrderItem
        fields = ['id', 'book_id', 'book_title', 'quantity', 'price', 'subtotal']


class OrderSerializer(serializers.ModelSerializer):
    """Serializer for Order model"""
    items = OrderItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = Order
        fields = ['id', 'user_id', 'status', 'total', 'items', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
