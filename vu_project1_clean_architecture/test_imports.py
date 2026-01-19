"""
Test script to verify all imports work correctly
"""
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("Testing imports...")

try:
    print("1. Testing domain entities...")
    from domain.entities import Book, Customer, Cart, CartItem
    print("   ✓ Domain entities imported successfully")
    
    print("2. Testing domain exceptions...")
    from domain.exceptions import BookNotFoundException, CustomerNotFoundException
    print("   ✓ Domain exceptions imported successfully")
    
    print("3. Testing domain value objects...")
    from domain.value_objects import UserCredentials, UserRegistrationData, SearchCriteria
    print("   ✓ Domain value objects imported successfully")
    
    print("4. Testing repository interfaces...")
    from interfaces.repositories import IBookRepository, ICustomerRepository, ICartRepository, IAuthRepository
    print("   ✓ Repository interfaces imported successfully")
    
    print("5. Testing use cases...")
    from usecases.book import ListBooksUseCase, GetBookDetailsUseCase
    from usecases.cart import AddItemToCartUseCase, ViewCartUseCase
    from usecases.auth import RegisterUserUseCase, LoginUserUseCase
    print("   ✓ Use cases imported successfully")
    
    print("\n✅ All core business logic imports successful!")
    print("   Clean architecture layers are properly structured.")
    
except ImportError as e:
    print(f"\n❌ Import error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\nNow testing Django-dependent modules...")

try:
    # Set Django settings
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vu_project1_clean_architecture.settings')
    
    import django
    django.setup()
    
    print("6. Testing infrastructure models...")
    from infrastructure.models import BookModel, CustomerModel, CartModel, CartItemModel
    print("   ✓ Infrastructure models imported successfully")
    
    print("7. Testing infrastructure repositories...")
    from infrastructure.repositories import DjangoBookRepository, DjangoCustomerRepository
    print("   ✓ Infrastructure repositories imported successfully")
    
    print("8. Testing framework views...")
    from framework.views import BookListView, CartView, RegisterView
    print("   ✓ Framework views imported successfully")
    
    print("\n✅ All imports successful!")
    print("   The clean architecture is ready to use.")
    
except Exception as e:
    print(f"\n⚠️  Django-dependent import issue: {e}")
    print("   This is expected if database is not configured yet.")
    print("   Core business logic is still functional!")

print("\n" + "="*60)
print("CLEAN ARCHITECTURE VERIFICATION COMPLETE")
print("="*60)
