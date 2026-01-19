"""
Domain Exceptions
Business logic exceptions for the domain layer
"""


class DomainException(Exception):
    """Base exception for domain layer"""
    pass


class EntityNotFoundException(DomainException):
    """Exception raised when an entity is not found"""
    def __init__(self, entity_name: str, entity_id: any):
        self.entity_name = entity_name
        self.entity_id = entity_id
        super().__init__(f"{entity_name} with id {entity_id} not found")


class BookNotFoundException(EntityNotFoundException):
    """Exception raised when a book is not found"""
    def __init__(self, book_id: int):
        super().__init__("Book", book_id)


class CustomerNotFoundException(EntityNotFoundException):
    """Exception raised when a customer is not found"""
    def __init__(self, customer_id: int):
        super().__init__("Customer", customer_id)


class CartNotFoundException(EntityNotFoundException):
    """Exception raised when a cart is not found"""
    def __init__(self, cart_id: int):
        super().__init__("Cart", cart_id)


class InsufficientStockException(DomainException):
    """Exception raised when book stock is insufficient"""
    def __init__(self, book_title: str, available: int, requested: int):
        self.book_title = book_title
        self.available = available
        self.requested = requested
        super().__init__(
            f"Insufficient stock for '{book_title}'. "
            f"Available: {available}, Requested: {requested}"
        )


class InvalidQuantityException(DomainException):
    """Exception raised when quantity is invalid"""
    def __init__(self, quantity: int):
        self.quantity = quantity
        super().__init__(f"Invalid quantity: {quantity}. Must be positive.")


class AuthenticationException(DomainException):
    """Exception raised for authentication failures"""
    pass


class InvalidCredentialsException(AuthenticationException):
    """Exception raised when credentials are invalid"""
    def __init__(self):
        super().__init__("Invalid username or password")


class UserAlreadyExistsException(DomainException):
    """Exception raised when user already exists"""
    def __init__(self, username: str):
        self.username = username
        super().__init__(f"User '{username}' already exists")


class ValidationException(DomainException):
    """Exception raised for validation errors"""
    def __init__(self, field: str, message: str):
        self.field = field
        self.message = message
        super().__init__(f"Validation error for '{field}': {message}")
