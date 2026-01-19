# Clean Architecture Diagram

## Layers Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                         FRAMEWORK LAYER                              │
│  (Django Views, Serializers, URLs - HTTP Controllers)              │
│  ┌─────────────────────────────────────────────────────────────┐  │
│  │  BookListView, CartView, RegisterView                       │  │
│  │  Handles HTTP requests/responses                            │  │
│  └─────────────────────────────────────────────────────────────┘  │
└────────────────────────────────┬────────────────────────────────────┘
                                 │ depends on
                                 ↓
┌─────────────────────────────────────────────────────────────────────┐
│                      INFRASTRUCTURE LAYER                            │
│  (Django ORM Models, Repository Implementations)                    │
│  ┌─────────────────────────────────────────────────────────────┐  │
│  │  DjangoBookRepository, DjangoCartRepository                 │  │
│  │  BookModel, CartModel (Django ORM)                          │  │
│  └─────────────────────────────────────────────────────────────┘  │
└────────────────────────────────┬────────────────────────────────────┘
                                 │ implements
                                 ↓
┌─────────────────────────────────────────────────────────────────────┐
│                        INTERFACES LAYER                              │
│  (Repository Interfaces - Contracts)                                │
│  ┌─────────────────────────────────────────────────────────────┐  │
│  │  IBookRepository, ICartRepository, IAuthRepository          │  │
│  │  Abstract interfaces defining data operations               │  │
│  └─────────────────────────────────────────────────────────────┘  │
└────────────────────────────────┬────────────────────────────────────┘
                                 │ used by
                                 ↓
┌─────────────────────────────────────────────────────────────────────┐
│                         USE CASES LAYER                              │
│  (Application Business Logic)                                       │
│  ┌─────────────────────────────────────────────────────────────┐  │
│  │  ListBooksUseCase, AddItemToCartUseCase                     │  │
│  │  Pure business logic - framework independent                │  │
│  └─────────────────────────────────────────────────────────────┘  │
└────────────────────────────────┬────────────────────────────────────┘
                                 │ operates on
                                 ↓
┌─────────────────────────────────────────────────────────────────────┐
│                          DOMAIN LAYER                                │
│  (Business Entities, Rules, Exceptions)                             │
│  ┌─────────────────────────────────────────────────────────────┐  │
│  │  Book, Customer, Cart entities                              │  │
│  │  Pure Python - no frameworks                                │  │
│  │  Contains core business rules                               │  │
│  └─────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
```

## Request Flow Example: Add Item to Cart

```
1. HTTP Request
   POST /api/cart/add/ {book_id: 1, quantity: 2}
   │
   ↓
2. Framework Layer (AddToCartView)
   - Validates request
   - Extracts user_id from authentication
   - Calls use case
   │
   ↓
3. Use Case Layer (AddItemToCartUseCase)
   - Gets customer via repository
   - Gets book via repository
   - Validates business rules (stock availability)
   - Updates cart entity
   - Saves via repository
   │
   ↓
4. Infrastructure Layer (DjangoCartRepository)
   - Translates domain entity to ORM model
   - Performs database operations
   - Returns domain entity
   │
   ↓
5. Framework Layer (AddToCartView)
   - Converts entity to JSON via serializer
   - Returns HTTP response
```

## Key Principles

### Dependency Rule
**Dependencies point INWARD only**
- Framework → Infrastructure → Interfaces ← Use Cases ← Domain
- Domain has ZERO dependencies
- Use Cases depend only on Domain and Interfaces
- Infrastructure implements Interfaces

### Single Responsibility
- **Domain**: Business entities and rules
- **Use Cases**: Application-specific business logic
- **Interfaces**: Define contracts
- **Infrastructure**: Technical implementations
- **Framework**: HTTP handling

### Open/Closed Principle
- Easy to add new use cases without modifying domain
- Easy to change infrastructure (swap database) without touching business logic

## Benefits Visualization

### Monolithic Architecture
```
┌─────────────────────────────────┐
│  Views (Django-aware)           │
│  ┌───────────────────────────┐  │
│  │ Business Logic mixed in   │  │
│  └───────────────────────────┘  │
│  ┌───────────────────────────┐  │
│  │ Django Models (ORM)       │  │
│  └───────────────────────────┘  │
└─────────────────────────────────┘
         Everything coupled!
```

### Clean Architecture
```
┌─────────────────────────────────┐
│  Framework (replaceable)        │
├─────────────────────────────────┤
│  Infrastructure (replaceable)   │
├─────────────────────────────────┤
│  Use Cases (testable)           │
├─────────────────────────────────┤
│  Domain (pure, stable)          │
└─────────────────────────────────┘
     Clear boundaries, easy to test!
```

## Testing Strategy

```
Domain Tests
├── Book entity validates stock
├── Cart calculates totals
└── No framework dependencies

Use Case Tests
├── AddItemToCartUseCase with mock repositories
├── Tests business logic only
└── Fast unit tests

Integration Tests
├── Repository implementations with real DB
├── Verify data persistence
└── Database fixtures

E2E Tests
├── Full HTTP request through all layers
├── Complete system behavior
└── Real database and server
```

## File Organization

```
project/
├── domain/                 # INNER CIRCLE
│   ├── entities/          # Business objects
│   ├── exceptions.py      # Business exceptions
│   └── value_objects.py   # Immutable values
│
├── usecases/              # APPLICATION LAYER
│   ├── book/             # Book-related use cases
│   ├── cart/             # Cart-related use cases
│   └── auth/             # Auth-related use cases
│
├── interfaces/            # INTERFACE ADAPTERS
│   └── repositories/     # Data access contracts
│
├── infrastructure/        # OUTER CIRCLE
│   ├── models.py         # Django ORM models
│   └── repositories/     # Repository implementations
│
└── framework/             # FRAMEWORKS & DRIVERS
    ├── views/            # HTTP controllers
    ├── serializers.py    # Response formatting
    ├── urls.py          # Routing
    └── dependencies.py   # Dependency injection
```

## Migration Comparison

### Before (Monolithic)
```python
# models.py - Django ORM models (framework-tied)
class Book(models.Model):
    title = models.CharField()
    
# services.py - Business logic with Django awareness
class BookService:
    def get_books():
        return Book.objects.all()  # Coupled to Django

# views.py - Controller with business logic
def book_list(request):
    books = Book.objects.filter(...)  # Mixed concerns
```

### After (Clean Architecture)
```python
# domain/entities/book.py - Pure Python
@dataclass
class Book:
    title: str
    def is_available(self): return self.stock > 0

# usecases/book/list_books.py - Business logic
class ListBooksUseCase:
    def execute(self, search):
        return self.repo.search(search)  # Uses interface

# infrastructure/repositories/book_repository_impl.py
class DjangoBookRepository(IBookRepository):
    def search(self, criteria):
        return BookModel.objects.filter(...)  # Django here

# framework/views/book_views.py - HTTP handling
class BookListView(APIView):
    def get(self, request):
        books = self.use_case.execute(search)
        return Response(serialize(books))
```

**Result**: Each layer has one responsibility and can be tested/changed independently!
