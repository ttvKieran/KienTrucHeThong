from rest_framework import serializers
from ..models import Rating, Book, Customer


class RatingSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source='customer.fullname', read_only=True)
    book_title = serializers.CharField(source='book.title', read_only=True)
    
    class Meta:
        model = Rating
        fields = ['id', 'customer', 'customer_name', 'book', 'book_title', 'score', 'review', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class CreateRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['book', 'score', 'review']
        
    def validate_score(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Score must be between 1 and 5")
        return value
