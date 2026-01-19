"""
Dependency Injection Container
Wires up all dependencies for clean architecture
"""
from infrastructure.repositories import (
    DjangoBookRepository,
    DjangoCustomerRepository,
    DjangoCartRepository,
    DjangoAuthRepository
)
from usecases.book import ListBooksUseCase, GetBookDetailsUseCase
from usecases.cart import (
    AddItemToCartUseCase,
    ViewCartUseCase,
    UpdateCartItemUseCase,
    RemoveItemFromCartUseCase
)
from usecases.auth import RegisterUserUseCase, LoginUserUseCase, GetUserProfileUseCase


class DependencyContainer:
    """
    Dependency Injection Container
    Manages all application dependencies
    """
    
    def __init__(self):
        # Initialize repositories (Infrastructure layer)
        self.book_repository = DjangoBookRepository()
        self.customer_repository = DjangoCustomerRepository()
        self.cart_repository = DjangoCartRepository()
        self.auth_repository = DjangoAuthRepository()
        
        # Initialize use cases (Application layer)
        self._init_book_use_cases()
        self._init_cart_use_cases()
        self._init_auth_use_cases()
    
    def _init_book_use_cases(self):
        """Initialize book-related use cases"""
        self.list_books_use_case = ListBooksUseCase(self.book_repository)
        self.get_book_details_use_case = GetBookDetailsUseCase(self.book_repository)
    
    def _init_cart_use_cases(self):
        """Initialize cart-related use cases"""
        self.add_item_to_cart_use_case = AddItemToCartUseCase(
            self.book_repository,
            self.customer_repository,
            self.cart_repository
        )
        self.view_cart_use_case = ViewCartUseCase(
            self.customer_repository,
            self.cart_repository
        )
        self.update_cart_item_use_case = UpdateCartItemUseCase(
            self.book_repository,
            self.customer_repository,
            self.cart_repository
        )
        self.remove_item_from_cart_use_case = RemoveItemFromCartUseCase(
            self.customer_repository,
            self.cart_repository
        )
    
    def _init_auth_use_cases(self):
        """Initialize auth-related use cases"""
        self.register_user_use_case = RegisterUserUseCase(self.auth_repository)
        self.login_user_use_case = LoginUserUseCase(self.auth_repository)
        self.get_user_profile_use_case = GetUserProfileUseCase(self.customer_repository)


# Global container instance
_container = None


def get_container() -> DependencyContainer:
    """Get or create global container instance"""
    global _container
    if _container is None:
        _container = DependencyContainer()
    return _container


def inject_dependencies(view_class):
    """
    Decorator to inject dependencies into view classes
    """
    original_init = view_class.__init__
    
    def new_init(self, **kwargs):
        original_init(self, **kwargs)
        container = get_container()
        
        # Inject use cases based on view class name
        if 'BookList' in view_class.__name__:
            self.list_books_use_case = container.list_books_use_case
        elif 'BookDetail' in view_class.__name__:
            self.get_book_details_use_case = container.get_book_details_use_case
        elif 'CartView' in view_class.__name__ and 'Add' not in view_class.__name__ and 'Update' not in view_class.__name__ and 'Remove' not in view_class.__name__:
            self.view_cart_use_case = container.view_cart_use_case
        elif 'AddToCart' in view_class.__name__:
            self.add_item_use_case = container.add_item_to_cart_use_case
        elif 'UpdateCartItem' in view_class.__name__:
            self.update_item_use_case = container.update_cart_item_use_case
        elif 'RemoveFromCart' in view_class.__name__:
            self.remove_item_use_case = container.remove_item_from_cart_use_case
        elif 'Register' in view_class.__name__:
            self.register_use_case = container.register_user_use_case
        elif 'Login' in view_class.__name__:
            self.login_use_case = container.login_user_use_case
        elif 'Profile' in view_class.__name__:
            self.get_profile_use_case = container.get_user_profile_use_case
    
    view_class.__init__ = new_init
    return view_class
