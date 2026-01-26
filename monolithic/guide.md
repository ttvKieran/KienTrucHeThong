# SETUP GUIDE - Bookstore Monolithic với MySQL

## 📋 **Yêu cầu hệ thống**

- Python 3.8+
- MySQL 8.0+
- pip

---

## 🚀 **Các bước cài đặt**

### **Bước 1: Cài đặt MySQL Client**

```bash
pip install mysqlclient
# Hoặc nếu gặp lỗi:
pip install pymysql
```

### **Bước 2: Tạo Database trong MySQL**

Mở MySQL và chạy:

```sql
CREATE DATABASE bookstore CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### **Bước 3: Cấu hình Database trong settings.py**

File `monolithic/settings.py` đã được cấu hình:

```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "bookstore",
        "USER": "root",
        "PASSWORD": "117788",  # Thay password của bạn
        "HOST": "localhost",
        "PORT": "3306",
        "OPTIONS": {
            "charset": "utf8mb4",
        },
    }
}
```

### **Bước 4: Tạo thư mục migrations**

```bash
cd store
mkdir migrations
New-Item -Path "migrations\__init__.py" -ItemType File
cd ..
```

Hoặc tạo thủ công:
- Tạo thư mục `store/migrations/`
- Tạo file rỗng `store/migrations/__init__.py`

### **Bước 5: Chạy Migrations**

```bash
# Tạo migrations
python manage.py makemigrations

# Xem SQL sẽ được tạo (optional)
python manage.py sqlmigrate store 0001

# Apply migrations
python manage.py migrate
```

### **Bước 6: Tạo Superuser**

```bash
python manage.py createsuperuser
```

Nhập:
- Username: admin
- Email: admin@example.com
- Password: (mật khẩu của bạn)

### **Bước 7: Tạo dữ liệu mẫu (Optional)**

Chạy trong Django shell:

```bash
python manage.py shell
```

Trong shell:

```python
from store.models import *

# Tạo categories
cat1 = Category.objects.create(name="Programming", description="Programming books")
cat2 = Category.objects.create(name="Fiction", description="Fiction books")

# Tạo shipping methods
ship1 = Shipping.objects.create(method_name="Standard Delivery", fee=5.0)
ship2 = Shipping.objects.create(method_name="Express Delivery", fee=10.0)

# Tạo payment methods
pay1 = Payment.objects.create(method_name="Cash on Delivery", status="Active")
pay2 = Payment.objects.create(method_name="Credit Card", status="Active")

# Tạo staff
staff1 = Staff.objects.create(name="Admin Staff", role="Manager")

# Tạo address
addr1 = Address.objects.create(
    house_number="123",
    building="Tower A",
    street="Nguyen Trai",
    province="Hanoi"
)

# Tạo customer
customer1 = Customer.objects.create(
    name="Nguyen Van A",
    email="customer@gmail.com",
    password="123456",
    address=addr1
)

# Tạo books
book1 = Book.objects.create(
    title="Clean Code",
    author="Robert Martin",
    price=45.99,
    stock_quantity=100,
    category=cat1
)

book2 = Book.objects.create(
    title="Design Patterns",
    author="Gang of Four",
    price=55.99,
    stock_quantity=50,
    category=cat1
)

print("Dữ liệu mẫu đã được tạo!")
exit()
```

### **Bước 8: Chạy Server**

```bash
python manage.py runserver
```

Truy cập:
- **Admin Panel:** http://127.0.0.1:8000/admin/
- **API Endpoint:** http://127.0.0.1:8000/api/

---

## 🧪 **Test API với cURL hoặc Postman**

### Test 1: Tìm kiếm sách
```bash
curl http://127.0.0.1:8000/api/books/search/?q=clean
```

### Test 2: Thêm sách vào giỏ hàng
```bash
curl -X POST http://127.0.0.1:8000/api/cart/1/add/ \
  -H "Content-Type: application/json" \
  -d '{"book_id": 1, "quantity": 2}'
```

### Test 3: Xem giỏ hàng
```bash
curl http://127.0.0.1:8000/api/cart/1/
```

### Test 4: Đặt hàng
```bash
curl -X POST http://127.0.0.1:8000/api/orders/create/1/ \
  -H "Content-Type: application/json" \
  -d '{"shipping_id": 1, "payment_id": 1, "staff_id": 1}'
```

### Test 5: Gợi ý sách
```bash
curl http://127.0.0.1:8000/api/recommendations/by-rating/?limit=5
```

---

## ❗ **Troubleshooting**

### Lỗi: Table doesn't exist
```bash
python manage.py migrate --run-syncdb
```

### Lỗi: No module named 'MySQLdb'
```bash
pip install mysqlclient
```

### Reset database
```sql
DROP DATABASE bookstore;
CREATE DATABASE bookstore CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

Sau đó chạy lại migrations:
```bash
python manage.py migrate
```

---

## 📁 **Cấu trúc Project**

```
monolithic/
├── controllers/           # Business logic
│   ├── bookController.py
│   ├── cartController.py
│   ├── customerController.py
│   ├── orderController.py
│   ├── staffController.py
│   └── recommendationController.py
├── store/                 # Django app
│   ├── models/           # Data models
│   │   ├── book.py
│   │   ├── customer.py
│   │   ├── order.py
│   │   ├── staff.py
│   │   └── __init__.py
│   ├── admin.py
│   └── apps.py
├── urls/                  # URL routing
│   ├── book_urls.py
│   ├── cart_urls.py
│   ├── customer_url.py
│   ├── order_urls.py
│   ├── staff_urls.py
│   └── recommendation_urls.py
├── monolithic/           # Django config
│   ├── settings.py
│   └── urls.py
└── manage.py
```

---

## ✅ **Checklist hoàn thành**

- [x] Models đã tạo
- [x] Controllers đã viết
- [x] URLs đã cấu hình
- [x] Admin đã đăng ký
- [ ] Migrations đã chạy
- [ ] Superuser đã tạo
- [ ] Dữ liệu mẫu đã thêm
- [ ] Server đã test
