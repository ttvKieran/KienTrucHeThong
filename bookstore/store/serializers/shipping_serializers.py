from rest_framework import serializers
from store.models import Shipping


class ShippingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shipping
        fields = ['id', 'method_name', 'fee', 'description', 'estimated_days', 'is_active']
        
    def validate_fee(self, value):
        if value < 0:
            raise serializers.ValidationError("Fee cannot be negative")
        return value
