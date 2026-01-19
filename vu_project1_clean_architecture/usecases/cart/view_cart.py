"""
View Cart Use Case
Business action: View customer's shopping cart
"""
from domain.entities import Cart
from domain.exceptions import CustomerNotFoundException
from interfaces.repositories import ICustomerRepository, ICartRepository


class ViewCartUseCase:
    """
    Use case for viewing cart
    Pure business logic
    """
    
    def __init__(
        self,
        customer_repository: ICustomerRepository,
        cart_repository: ICartRepository
    ):
        self.customer_repository = customer_repository
        self.cart_repository = cart_repository
    
    def execute(self, user_id: int) -> Cart:
        """
        Execute use case to view cart
        
        Args:
            user_id: User ID
            
        Returns:
            Cart with items
            
        Raises:
            CustomerNotFoundException: If customer not found
        """
        # Get customer
        customer = self.customer_repository.get_by_user_id(user_id)
        if customer is None:
            raise CustomerNotFoundException(user_id)
        
        # Get cart
        cart = self.cart_repository.get_by_customer_id(customer.id)
        
        # Return empty cart if not exists
        if cart is None:
            cart = Cart(id=None, customer_id=customer.id, items=[])
        
        return cart
