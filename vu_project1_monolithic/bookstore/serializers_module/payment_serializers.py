from rest_framework import serializers
from ..models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Payment
        fields = ['id', 'method_name', 'status', 'status_display', 'transaction_id', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class CreatePaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['method_name', 'transaction_id']
