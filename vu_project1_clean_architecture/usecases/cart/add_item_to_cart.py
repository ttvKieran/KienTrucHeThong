"""
Add Item to Cart Use Case
Business action: Add book to customer's shopping cart
"""
from decimal import Decimal
from domain.entities import Cart, CartItem
from domain.exceptions import BookNotFoundException, CustomerNotFoundException, InsufficientStockException
from interfaces.repositories import IBookRepository, ICustomerRepository, ICartRepository


class AddItemToCartUseCase:
    """
    Use case for adding item to cart
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
    
    def execute(self, user_id: int, book_id: int, quantity: int) -> Cart:
        """
        Execute use case to add item to cart
        
        Args:
            user_id: User ID
            book_id: Book ID to add
            quantity: Quantity to add
            
        Returns:
            Updated cart
            
        Raises:
            CustomerNotFoundException: If customer not found
            BookNotFoundException: If book not found
            InsufficientStockException: If not enough stock
        """
        # Get customer
        customer = self.customer_repository.get_by_user_id(user_id)
        if customer is None:
            raise CustomerNotFoundException(user_id)
        
        # Get book
        book = self.book_repository.get_by_id(book_id)
        if book is None:
            raise BookNotFoundException(book_id)
        
        # Business rule: Check stock availability
        if not book.has_sufficient_stock(quantity):
            raise InsufficientStockException(book.title, book.stock, quantity)
        
        # Get or create cart
        cart = self.cart_repository.get_by_customer_id(customer.id)
        if cart is None:
            cart = Cart(id=None, customer_id=customer.id, items=[])
        
        # Check if adding to existing item
        existing_item = cart.get_item(book_id)
        if existing_item:
            new_quantity = existing_item.quantity + quantity
            if not book.has_sufficient_stock(new_quantity):
                raise InsufficientStockException(
                    book.title,
                    book.stock,
                    new_quantity
                )
        
        # Add item to cart (domain logic)
        # Using stock value as price for simplicity (as per original code)
        cart.add_item(book_id, book.title, quantity, Decimal(str(book.stock)))
        
        # Save cart
        saved_cart = self.cart_repository.save(cart)
        
        return saved_cart
