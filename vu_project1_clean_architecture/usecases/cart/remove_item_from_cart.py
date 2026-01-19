"""
Remove Item from Cart Use Case
Business action: Remove item from shopping cart
"""
from domain.entities import Cart
from domain.exceptions import CustomerNotFoundException, BookNotFoundException
from interfaces.repositories import ICustomerRepository, ICartRepository


class RemoveItemFromCartUseCase:
    """
    Use case for removing item from cart
    Pure business logic
    """
    
    def __init__(
        self,
        customer_repository: ICustomerRepository,
        cart_repository: ICartRepository
    ):
        self.customer_repository = customer_repository
        self.cart_repository = cart_repository
    
    def execute(self, user_id: int, book_id: int) -> Cart:
        """
        Execute use case to remove item from cart
        
        Args:
            user_id: User ID
            book_id: Book ID to remove
            
        Returns:
            Updated cart
            
        Raises:
            CustomerNotFoundException: If customer not found
            BookNotFoundException: If item not in cart
        """
        # Get customer
        customer = self.customer_repository.get_by_user_id(user_id)
        if customer is None:
            raise CustomerNotFoundException(user_id)
        
        # Get cart
        cart = self.cart_repository.get_by_customer_id(customer.id)
        if cart is None:
            raise BookNotFoundException(book_id)
        
        # Remove item (domain logic)
        removed = cart.remove_item(book_id)
        if not removed:
            raise BookNotFoundException(book_id)
        
        # Save cart
        saved_cart = self.cart_repository.save(cart)
        
        return saved_cart
