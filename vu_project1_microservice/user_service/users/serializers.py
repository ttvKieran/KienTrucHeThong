"""
User Serializers
"""
from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User, Customer


class CustomerSerializer(serializers.ModelSerializer):
    """Serializer for Customer model"""
    
    class Meta:
        model = Customer
        fields = ['id', 'fullname', 'address', 'phone', 'note', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate_fullname(self, value):
        if not value or len(value.strip()) == 0:
            raise serializers.ValidationError("Fullname cannot be empty")
        return value
    
    def validate_address(self, value):
        if not value or len(value.strip()) == 0:
            raise serializers.ValidationError("Address cannot be empty")
        return value
    
    def validate_phone(self, value):
        if not value or len(value.strip()) == 0:
            raise serializers.ValidationError("Phone cannot be empty")
        
        phone_clean = value.replace('+', '').replace('-', '').replace(' ', '')
        if not phone_clean.isdigit():
            raise serializers.ValidationError("Invalid phone number format")
        
        return value


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model"""
    customer_profile = CustomerSerializer(read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'customer_profile']
        read_only_fields = ['id']


class RegisterSerializer(serializers.Serializer):
    """Serializer for user registration"""
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=6)
    fullname = serializers.CharField(max_length=255)
    address = serializers.CharField()
    phone = serializers.CharField(max_length=20)
    note = serializers.CharField(required=False, allow_blank=True)
    
    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists")
        return value
    
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists")
        return value
    
    def create(self, validated_data):
        # Extract customer data
        customer_data = {
            'fullname': validated_data.pop('fullname'),
            'address': validated_data.pop('address'),
            'phone': validated_data.pop('phone'),
            'note': validated_data.pop('note', ''),
        }
        
        # Create user
        user = User.objects.create_user(**validated_data)
        
        # Create customer profile
        Customer.objects.create(user=user, **customer_data)
        
        return user


class LoginSerializer(serializers.Serializer):
    """Serializer for user login"""
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise serializers.ValidationError("Invalid credentials")
            if not user.is_active:
                raise serializers.ValidationError("User account is disabled")
            data['user'] = user
        else:
            raise serializers.ValidationError("Must include username and password")
        
        return data


class ProfileUpdateSerializer(serializers.Serializer):
    """Serializer for updating user profile"""
    fullname = serializers.CharField(max_length=255, required=False)
    address = serializers.CharField(required=False)
    phone = serializers.CharField(max_length=20, required=False)
    note = serializers.CharField(required=False, allow_blank=True)
