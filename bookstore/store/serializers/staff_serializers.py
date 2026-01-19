from rest_framework import serializers
from store.models import Staff
from django.contrib.auth.models import User


class StaffSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    
    class Meta:
        model = Staff
        fields = ['id', 'user', 'username', 'email', 'name', 'role', 'phone', 'hire_date']
        read_only_fields = ['hire_date']


class CreateStaffSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    email = serializers.EmailField(write_only=True)
    
    class Meta:
        model = Staff
        fields = ['username', 'password', 'email', 'name', 'role', 'phone']
    
    def create(self, validated_data):
        username = validated_data.pop('username')
        password = validated_data.pop('password')
        email = validated_data.pop('email')
        
        # Create User
        user = User.objects.create_user(
            username=username,
            password=password,
            email=email,
            is_staff=True
        )
        
        # Create Staff
        staff = Staff.objects.create(user=user, **validated_data)
        return staff
