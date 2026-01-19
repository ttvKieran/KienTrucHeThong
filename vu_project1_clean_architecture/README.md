# Bookstore Clean Architecture

This project demonstrates Clean Architecture principles applied to a Django bookstore application.

## Architecture Layers

### 1. Domain Layer (`domain/`)
- **Entities**: Pure business objects (Book, Customer, Cart, CartItem)
- **Value Objects**: Immutable objects representing domain concepts
- **Exceptions**: Business logic exceptions
- **No framework dependencies** - Pure Python

### 2. Use Cases Layer (`usecases/`)
- **Book Use Cases**: ListBooks, GetBookDetails
- **Cart Use Cases**: AddItemToCart, ViewCart, UpdateCartItem, RemoveItemFromCart
- **Auth Use Cases**: RegisterUser, LoginUser, GetUserProfile
- **Pure business logic** - Independent of frameworks

### 3. Interfaces Layer (`interfaces/`)
- **Repository Interfaces**: Abstract contracts for data access
  - IBookRepository
  - ICustomerRepository
  - ICartRepository
  - IAuthRepository
- **Defines what data operations are needed** without implementation details

### 4. Infrastructure Layer (`infrastructure/`)
- **Django ORM Models**: Framework-specific database models
- **Repository Implementations**: Concrete implementations using Django ORM
  - DjangoBookRepository
  - DjangoCustomerRepository
  - DjangoCartRepository
  - DjangoAuthRepository
- **Framework-dependent** - Isolated from business logic

### 5. Framework Layer (`framework/`)
- **Views/Controllers**: HTTP request handlers
- **Serializers**: Convert entities to JSON
- **URLs**: Route configuration
- **Dependency Injection**: Wires up all components

## Setup Instructions

### Prerequisites
- Python 3.11+
- MySQL 8.0+
- pip

### 1. Install Dependencies
```bash
cd vu_project1_clean_architecture
pip install -r requirements.txt
```

### 2. Configure MySQL Database
Create MySQL database (using MySQL CLI or MySQL Workbench):
```sql
CREATE DATABASE bookstore_clean_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

Or use the provided SQL file:
```bash
mysql -u root -p < create_db.sql
```

### 3. Update Database Settings (if needed)
Edit `vu_project1_clean_architecture/settings.py`:
```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "bookstore_clean_db",
        "USER": "root",           # Change if different
        "PASSWORD": "root",       # Change to your MySQL password
        "HOST": "localhost",
        "PORT": "3306",
    }
}
```

### 4. Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create Superuser (Optional)
```bash
python manage.py createsuperuser
```

### 6. Run Development Server
```bash
python manage.py runserver
```

The API will be available at: `http://localhost:8000/api/`

## API Endpoints

### Authentication
- **POST** `/api/auth/register/` - Register new user
  ```json
  {
    "username": "john_doe",
    "password": "password123",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "fullname": "John Doe",
    "address": "123 Main St",
    "phone": "+1234567890",
    "note": "Optional note"
  }
  ```

- **POST** `/api/auth/login/` - Login user
  ```json
  {
    "username": "john_doe",
    "password": "password123"
  }
  ```

- **GET** `/api/auth/profile/` - Get user profile (requires authentication)
  - Header: `Authorization: Token <your_token>`

### Books
- **GET** `/api/books/` - List all books
  - Query params: `?search=keyword&in_stock=true`

- **GET** `/api/books/<id>/` - Get book details

### Shopping Cart (All endpoints require authentication)
- **GET** `/api/cart/` - View cart
  - Header: `Authorization: Token <your_token>`

- **POST** `/api/cart/add/` - Add item to cart
  ```json
  {
    "book_id": 1,
    "quantity": 2
  }
  ```

- **PUT** `/api/cart/update/<book_id>/` - Update cart item quantity
  ```json
  {
    "quantity": 3
  }
  ```

- **DELETE** `/api/cart/remove/<book_id>/` - Remove item from cart

## Project Structure

```
vu_project1_clean_architecture/
├── domain/                          # Domain Layer (Business Entities)
│   ├── entities/
│   │   ├── book.py                 # Book entity with business logic
│   │   ├── customer.py             # Customer entity
│   │   └── cart.py                 # Cart and CartItem entities
│   ├── exceptions.py               # Business exceptions
│   └── value_objects.py            # Immutable value objects
│
├── usecases/                        # Use Cases Layer (Business Logic)
│   ├── book/
│   │   ├── list_books.py          # List books use case
│   │   └── get_book_details.py    # Get book details use case
│   ├── cart/
│   │   ├── add_item_to_cart.py    # Add to cart use case
│   │   ├── view_cart.py           # View cart use case
│   │   ├── update_cart_item.py    # Update cart item use case
│   │   └── remove_item_from_cart.py # Remove from cart use case
│   └── auth/
│       ├── register_user.py       # User registration use case
│       ├── login_user.py          # User login use case
│       └── get_user_profile.py    # Get profile use case
│
├── interfaces/                      # Interfaces Layer (Contracts)
│   └── repositories/
│       ├── book_repository.py     # Book repository interface
│       ├── customer_repository.py  # Customer repository interface
│       ├── cart_repository.py     # Cart repository interface
│       └── auth_repository.py     # Auth repository interface
│
├── infrastructure/                  # Infrastructure Layer (Framework)
│   ├── models.py                  # Django ORM models
│   └── repositories/
│       ├── book_repository_impl.py       # Book repo implementation
│       ├── customer_repository_impl.py   # Customer repo implementation
│       ├── cart_repository_impl.py       # Cart repo implementation
│       └── auth_repository_impl.py       # Auth repo implementation
│
├── framework/                       # Framework Layer (Django)
│   ├── views/
│   │   ├── book_views.py          # Book HTTP controllers
│   │   ├── cart_views.py          # Cart HTTP controllers
│   │   └── auth_views.py          # Auth HTTP controllers
│   ├── serializers.py             # DRF serializers
│   ├── urls.py                    # URL routing
│   └── dependencies.py            # Dependency injection container
│
└── vu_project1_clean_architecture/  # Django project settings
    ├── settings.py                # Project configuration
    └── urls.py                    # Root URL configuration
```

## Clean Architecture Benefits

### 1. **Separation of Concerns**
Each layer has a specific responsibility and doesn't know about layers above it.

### 2. **Testability**
Business logic can be tested without Django, databases, or HTTP.

### 3. **Framework Independence**
Domain and use case layers are pure Python - can switch frameworks easily.

### 4. **Database Independence**
Can swap MySQL for PostgreSQL, MongoDB, etc. by changing only infrastructure layer.

### 5. **Screaming Architecture**
Project structure immediately tells you it's a bookstore application with books, carts, and authentication.

### 6. **Business Logic Protection**
All business rules are in entities and use cases - easy to find and maintain.

## Dependency Flow

```
Framework → Infrastructure → Use Cases → Domain
(Django)    (Repositories)   (Logic)     (Entities)
```

**Dependencies point inward** - Domain has no dependencies on outer layers.

## Testing Strategy

### Unit Tests
- Test domain entities in isolation
- Test use cases with mock repositories
- No framework dependencies needed

### Integration Tests
- Test repository implementations with real database
- Test that infrastructure correctly implements interfaces

### End-to-End Tests
- Test full request/response cycle through framework layer
- Verify complete system behavior

## Comparison with Monolithic

### Monolithic (`vu_project1`)
```
bookstore/
├── models.py           # Django models (framework-tied)
├── services/           # Business logic (framework-aware)
└── views.py            # Controllers (tightly coupled)
```
**Issues:**
- Business logic mixed with framework code
- Hard to test without Django
- Difficult to change database or framework
- No clear boundaries

### Clean Architecture (`vu_project1_clean_architecture`)
```
domain/ → interfaces/ → usecases/ → infrastructure/ → framework/
(Pure)    (Contracts)   (Logic)     (Django ORM)      (HTTP)
```
**Benefits:**
- Clear separation of concerns
- Framework-independent business logic
- Easy to test each layer
- Can swap frameworks/databases
- Screaming architecture

## Adding New Features

### Example: Add "Checkout" Feature

1. **Domain**: Create `Order` entity with validation
2. **Interfaces**: Define `IOrderRepository` interface
3. **Use Case**: Implement `CheckoutUseCase` with business logic
4. **Infrastructure**: Implement `DjangoOrderRepository`
5. **Framework**: Create `CheckoutView` controller

Each step is independent and testable!

## License
Educational project for demonstrating Clean Architecture principles.
