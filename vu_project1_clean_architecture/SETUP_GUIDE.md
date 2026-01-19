# Setup and Testing Guide

## Complete Setup Steps

### Step 1: Install MySQL Client
Make sure MySQL is installed and running on your system.

### Step 2: Create Database
```sql
-- Option 1: Using MySQL CLI
mysql -u root -p
CREATE DATABASE bookstore_clean_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
exit;

-- Option 2: Using the provided SQL file
mysql -u root -p < create_db.sql
```

### Step 3: Install Python Dependencies
```bash
cd vu_project1_clean_architecture
pip install -r requirements.txt
```

Required packages:
- Django==5.1.1
- djangorestframework==3.14.0
- mysqlclient==2.2.0

### Step 4: Update Database Configuration
If your MySQL credentials are different, edit `vu_project1_clean_architecture/settings.py`:

```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "bookstore_clean_db",
        "USER": "your_mysql_user",      # Change this
        "PASSWORD": "your_password",     # Change this
        "HOST": "localhost",
        "PORT": "3306",
    }
}
```

### Step 5: Run Migrations
```bash
# Create migration files
python manage.py makemigrations infrastructure

# Apply migrations to database
python manage.py migrate
```

Expected output:
```
Operations to perform:
  Apply all migrations: admin, auth, authtoken, contenttypes, infrastructure, sessions
Running migrations:
  Applying infrastructure.0001_initial... OK
  ...
```

### Step 6: Create Sample Data (Optional)
```bash
python manage.py shell
```

Then in the shell:
```python
from infrastructure.models import BookModel
from django.utils.text import slugify

# Create sample books
books = [
    {"title": "Clean Architecture", "author": "Robert C. Martin", "stock": 10},
    {"title": "Design Patterns", "author": "Gang of Four", "stock": 5},
    {"title": "Domain-Driven Design", "author": "Eric Evans", "stock": 8},
]

for book_data in books:
    BookModel.objects.create(
        title=book_data["title"],
        author=book_data["author"],
        stock=book_data["stock"],
        slug=slugify(book_data["title"])
    )

print("Sample books created!")
exit()
```

### Step 7: Create Admin User (Optional)
```bash
python manage.py createsuperuser
```

Follow the prompts to create an admin account.

### Step 8: Run Development Server
```bash
python manage.py runserver
```

Server will start at: `http://localhost:8000/`

## Testing the API

### 1. Test Book Endpoints (No Authentication Required)

**List all books:**
```bash
curl http://localhost:8000/api/books/
```

**Search books:**
```bash
curl "http://localhost:8000/api/books/?search=clean"
```

**Filter in-stock books:**
```bash
curl "http://localhost:8000/api/books/?in_stock=true"
```

**Get book details:**
```bash
curl http://localhost:8000/api/books/1/
```

### 2. Test Authentication

**Register new user:**
```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "testpass123",
    "email": "test@example.com",
    "fullname": "Test User",
    "address": "123 Test Street",
    "phone": "+1234567890"
  }'
```

Response:
```json
{
  "user_id": 1,
  "customer_id": 1,
  "token": "abc123...",
  "message": "User registered successfully"
}
```

**Login:**
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "testpass123"
  }'
```

Response:
```json
{
  "user_id": 1,
  "token": "abc123...",
  "message": "Login successful"
}
```

**Get profile (requires token):**
```bash
curl http://localhost:8000/api/auth/profile/ \
  -H "Authorization: Token abc123..."
```

### 3. Test Cart Operations (Require Authentication)

**View cart:**
```bash
curl http://localhost:8000/api/cart/ \
  -H "Authorization: Token abc123..."
```

**Add item to cart:**
```bash
curl -X POST http://localhost:8000/api/cart/add/ \
  -H "Authorization: Token abc123..." \
  -H "Content-Type: application/json" \
  -d '{
    "book_id": 1,
    "quantity": 2
  }'
```

**Update cart item:**
```bash
curl -X PUT http://localhost:8000/api/cart/update/1/ \
  -H "Authorization: Token abc123..." \
  -H "Content-Type: application/json" \
  -d '{
    "quantity": 5
  }'
```

**Remove from cart:**
```bash
curl -X DELETE http://localhost:8000/api/cart/remove/1/ \
  -H "Authorization: Token abc123..."
```

## Using Postman

### Setup
1. Open Postman
2. Create new collection "Bookstore API"
3. Set base URL: `http://localhost:8000/api`

### Authentication Setup
1. Register or login to get token
2. For protected endpoints, add header:
   - Key: `Authorization`
   - Value: `Token <your_token>`

### Example Requests

**1. Register:**
- Method: POST
- URL: `{{base_url}}/auth/register/`
- Body (JSON):
```json
{
  "username": "john_doe",
  "password": "password123",
  "email": "john@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "fullname": "John Doe",
  "address": "123 Main St, New York, NY",
  "phone": "+1234567890",
  "note": "Test account"
}
```

**2. Login:**
- Method: POST
- URL: `{{base_url}}/auth/login/`
- Body (JSON):
```json
{
  "username": "john_doe",
  "password": "password123"
}
```
- Save the token from response

**3. List Books:**
- Method: GET
- URL: `{{base_url}}/books/`

**4. Add to Cart:**
- Method: POST
- URL: `{{base_url}}/cart/add/`
- Headers: `Authorization: Token <token>`
- Body (JSON):
```json
{
  "book_id": 1,
  "quantity": 2
}
```

## Troubleshooting

### Database Connection Error
```
django.db.utils.OperationalError: (2003, "Can't connect to MySQL server")
```
**Solution:**
- Ensure MySQL is running
- Check database credentials in settings.py
- Verify database exists: `SHOW DATABASES;` in MySQL

### Import Errors
```
ModuleNotFoundError: No module named 'domain'
```
**Solution:**
- Ensure you're in the correct directory
- Check INSTALLED_APPS includes 'infrastructure'
- Verify Python path is set correctly in settings.py

### Token Authentication Not Working
```
{"detail": "Authentication credentials were not provided."}
```
**Solution:**
- Include header: `Authorization: Token <your_token>`
- Ensure token is valid (login again if needed)

### Migration Errors
```
django.db.migrations.exceptions.InconsistentMigrationHistory
```
**Solution:**
```bash
# Reset migrations (careful - drops data!)
python manage.py migrate infrastructure zero
python manage.py makemigrations infrastructure
python manage.py migrate
```

## Running Unit Tests

Create test files to verify each layer:

### Test Domain Entities
```python
# tests/test_domain.py
from domain.entities import Book

def test_book_validation():
    book = Book(id=1, title="Test", author="Author", stock=5)
    assert book.is_available() == True
    
def test_insufficient_stock():
    book = Book(id=1, title="Test", author="Author", stock=2)
    assert book.has_sufficient_stock(3) == False
```

### Test Use Cases
```python
# tests/test_usecases.py
from usecases.book import ListBooksUseCase
from unittest.mock import Mock

def test_list_books_use_case():
    # Mock repository
    mock_repo = Mock()
    mock_repo.get_all.return_value = [...]
    
    # Test use case
    use_case = ListBooksUseCase(mock_repo)
    books = use_case.execute()
    
    assert len(books) > 0
```

Run tests:
```bash
python manage.py test
```

## Next Steps

1. **Add more features:**
   - Order checkout
   - Payment processing
   - Book reviews
   - Wishlist

2. **Improve security:**
   - JWT authentication
   - Rate limiting
   - Input validation

3. **Add caching:**
   - Redis for cart
   - Cache popular books

4. **Deploy:**
   - Docker containerization
   - Production database
   - Environment variables

## Additional Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Clean Architecture Book](https://www.amazon.com/Clean-Architecture-Craftsmans-Software-Structure/dp/0134494164)
