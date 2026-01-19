"""
Customer Repository Implementation
Infrastructure layer - implements repository interface using Django ORM
"""
from typing import Optional
from domain.entities import Customer
from interfaces.repositories import ICustomerRepository
from infrastructure.models import CustomerModel


class DjangoCustomerRepository(ICustomerRepository):
    """
    Django ORM implementation of Customer repository
    """
    
    def _to_entity(self, model: CustomerModel) -> Customer:
        """Convert Django model to domain entity"""
        return Customer(
            id=model.id,
            user_id=model.user.id,
            fullname=model.fullname,
            address=model.address,
            phone=model.phone,
            note=model.note
        )
    
    def _to_model(self, entity: Customer, model: CustomerModel = None) -> CustomerModel:
        """Convert domain entity to Django model"""
        from django.contrib.auth.models import User
        
        if model is None:
            model = CustomerModel()
            model.user = User.objects.get(id=entity.user_id)
        
        model.fullname = entity.fullname
        model.address = entity.address
        model.phone = entity.phone
        model.note = entity.note
        
        return model
    
    def get_by_id(self, customer_id: int) -> Optional[Customer]:
        """Get customer by ID"""
        try:
            model = CustomerModel.objects.get(id=customer_id)
            return self._to_entity(model)
        except CustomerModel.DoesNotExist:
            return None
    
    def get_by_user_id(self, user_id: int) -> Optional[Customer]:
        """Get customer by user ID"""
        try:
            model = CustomerModel.objects.get(user__id=user_id)
            return self._to_entity(model)
        except CustomerModel.DoesNotExist:
            return None
    
    def save(self, customer: Customer) -> Customer:
        """Save or update customer"""
        if customer.id:
            # Update existing
            try:
                model = CustomerModel.objects.get(id=customer.id)
                model = self._to_model(customer, model)
            except CustomerModel.DoesNotExist:
                model = self._to_model(customer)
        else:
            # Create new
            model = self._to_model(customer)
        
        model.save()
        return self._to_entity(model)
    
    def delete(self, customer_id: int) -> bool:
        """Delete customer by ID"""
        try:
            model = CustomerModel.objects.get(id=customer_id)
            model.delete()
            return True
        except CustomerModel.DoesNotExist:
            return False
