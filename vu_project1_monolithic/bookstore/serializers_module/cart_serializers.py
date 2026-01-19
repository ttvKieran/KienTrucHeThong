from rest_framework import serializers
from ..models import Cart, CartItem, Book


class CartItemSerializer(serializers.ModelSerializer):
    book_title = serializers.CharField(source='book.title', read_only=True)
    book_author = serializers.CharField(source='book.author', read_only=True)
    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ('id', 'book', 'book_title', 'book_author', 'quantity', 'price', 'subtotal')
        read_only_fields = ('price',)

    def get_subtotal(self, obj):
        return obj.quantity * obj.price


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(source='cartitem_set', many=True, read_only=True)
    total_items = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ('id', 'customer', 'created_at', 'items', 'total_items', 'total_price')
        read_only_fields = ('customer', 'created_at')

    def get_total_items(self, obj):
        return obj.cartitem_set.count()

    def get_total_price(self, obj):
        return sum(item.quantity * item.price for item in obj.cartitem_set.all())


class AddToCartSerializer(serializers.Serializer):
    book_id = serializers.IntegerField(required=True)
    quantity = serializers.IntegerField(required=True, min_value=1)

    def validate_book_id(self, value):
        try:
            Book.objects.get(id=value)
        except Book.DoesNotExist:
            raise serializers.ValidationError("Book not found")
        return value
