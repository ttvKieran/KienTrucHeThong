from rest_framework import serializers
from ..models import Order, OrderItem, Book, Shipping, Payment
from .shipping_serializers import ShippingSerializer
from .payment_serializers import PaymentSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    book_title = serializers.CharField(source='book.title', read_only=True)
    book_author = serializers.CharField(source='book.author', read_only=True)
    
    class Meta:
        model = OrderItem
        fields = ['id', 'book', 'book_title', 'book_author', 'quantity', 'price', 'subtotal']
        read_only_fields = ['subtotal']


class OrderSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source='customer.fullname', read_only=True)
    items = OrderItemSerializer(many=True, read_only=True)
    shipping_details = ShippingSerializer(source='shipping', read_only=True)
    payment_details = PaymentSerializer(source='payment', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Order
        fields = [
            'id', 'customer', 'customer_name', 'total_price', 'status', 'status_display',
            'shipping', 'shipping_details', 'payment', 'payment_details',
            'shipping_address', 'note', 'items', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class CreateOrderItemSerializer(serializers.Serializer):
    book_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)
    
    def validate_book_id(self, value):
        try:
            book = Book.objects.get(id=value)
        except Book.DoesNotExist:
            raise serializers.ValidationError("Book does not exist")
        return value


class CreateOrderSerializer(serializers.Serializer):
    """
    Serializer for creating an order from the customer's cart
    """
    shipping_id = serializers.IntegerField()
    payment_method = serializers.CharField(max_length=100)
    shipping_address = serializers.CharField()
    note = serializers.CharField(required=False, allow_blank=True)
    
    def validate_shipping_id(self, value):
        try:
            shipping = Shipping.objects.get(id=value, is_active=True)
        except Shipping.DoesNotExist:
            raise serializers.ValidationError("Shipping method does not exist or is not active")
        return value