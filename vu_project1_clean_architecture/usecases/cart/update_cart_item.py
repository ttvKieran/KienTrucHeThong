"""
Update Cart Item Use Case
Business action: Update quantity of item in cart
"""
from domain.entities import Cart
from domain.exceptions import CustomerNotFoundException, BookNotFoundException, InsufficientStockException
from interfaces.repositories import IBookRepository, ICustomerRepository, ICartRepository


class UpdateCartItemUseCase:
    """
    Use case for updating cart item quantity
    Pure business logic
    """
    
    def __init__(
        self,
        book_repository: IBookRepository,
        customer_repository: ICustomerRepository,
        cart_repository: ICartRepository
    ):
        self.book_repository = book_repository
        self.customer_repository = customer_repository
        self.cart_repository = cart_repository
    
    def execute(self, user_id: int, book_id: int, new_quantity: int) -> Cart:
        """
        Execute use case to update cart item quantity
        
        Args:
            user_id: User ID
            book_id: Book ID
            new_quantity: New quantity
            
        Returns:
            Updated cart
            
        Raises:
            CustomerNotFoundException: If customer not found
            BookNotFoundException: If book not found or not in cart
            InsufficientStockException: If not enough stock
        """
        # Get customer
        customer = self.customer_repository.get_by_user_id(user_id)
        if customer is None:
            raise CustomerNotFoundException(user_id)
        
        # Get cart
        cart = self.cart_repository.get_by_customer_id(customer.id)
        if cart is None:
            raise BookNotFoundException(book_id)  # No cart means no item
        
        # Check if item exists in cart
        item = cart.get_item(book_id)
        if item is None:
            raise BookNotFoundException(book_id)
        
        # Get book to check stock
        book = self.book_repository.get_by_id(book_id)
        if book is None:
            raise BookNotFoundException(book_id)
        
        # Business rule: Check stock availability
        if not book.has_sufficient_stock(new_quantity):
            raise InsufficientStockException(book.title, book.stock, new_quantity)
        
        # Update quantity (domain logic)
        cart.update_item_quantity(book_id, new_quantity)
        
        # Save cart
        saved_cart = self.cart_repository.save(cart)
        
        return saved_cart
