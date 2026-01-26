# API Documentation - Bookstore Monolithic

## Base URL
```
http://127.0.0.1:8000/api
```

---

## 📚 **BOOKS API** - `/api/books/`

### 1. Lấy danh sách tất cả sách
```http
GET /api/books/
```
**Response:**
```json
[
  {
    "id": 1,
    "title": "Clean Code",
    "author": "Robert Martin",
    "price": 45.99,
    "stock_quantity": 100,
    "category": "Programming",
    "category_id": 1
  }
]
```

### 2. Tìm kiếm sách
```http
GET /api/books/search/?q=clean&category=1
```
**Parameters:**
- `q`: Tìm theo title hoặc author
- `category`: Filter theo category ID

### 3. Xem chi tiết sách
```http
GET /api/books/1/
```
**Response:**
```json
{
  "id": 1,
  "title": "Clean Code",
  "author": "Robert Martin",
  "price": 45.99,
  "stock_quantity": 100,
  "category": "Programming",
  "category_id": 1,
  "average_rating": 4.5
}
```

### 4. Lấy danh sách categories
```http
GET /api/books/categories/
```

### 5. Thêm rating cho sách
```http
POST /api/books/1/rating/add/
Content-Type: application/json

{
  "customer_id": 1,
  "score": 4.5
}
```

### 6. Xem ratings của sách
```http
GET /api/books/1/ratings/
```

---

## 👥 **CUSTOMERS API** - `/api/customers/`

### 1. Đăng ký khách hàng mới
```http
POST /api/customers/register/
Content-Type: application/json

{
  "name": "Nguyen Van A",
  "email": "nguyenvana@gmail.com",
  "password": "password123",
  "address": {
    "house_number": "123",
    "building": "Building A",
    "street": "Nguyen Trai",
    "province": "Hanoi"
  }
}
```

### 2. Xem thông tin khách hàng
```http
GET /api/customers/1/
```

### 3. Cập nhật thông tin khách hàng
```http
PUT /api/customers/1/update/
Content-Type: application/json

{
  "name": "Nguyen Van B",
  "email": "newemail@gmail.com"
}
```

### 4. Lấy danh sách khách hàng
```http
GET /api/customers/
```

---

## 🛒 **CART API** - `/api/cart/`

### 1. Xem giỏ hàng
```http
GET /api/cart/1/
```
**Response:**
```json
{
  "cart_id": 1,
  "customer_id": 1,
  "items": [
    {
      "id": 1,
      "book_id": 1,
      "book_title": "Clean Code",
      "book_price": 45.99,
      "quantity": 2,
      "subtotal": 91.98
    }
  ],
  "total": 91.98
}
```

### 2. Tạo giỏ hàng mới
```http
POST /api/cart/1/create/
```

### 3. Thêm sách vào giỏ hàng
```http
POST /api/cart/1/add/
Content-Type: application/json

{
  "book_id": 1,
  "quantity": 2
}
```

### 4. Cập nhật số lượng trong giỏ hàng
```http
PUT /api/cart/items/1/update/
Content-Type: application/json

{
  "quantity": 3
}
```

### 5. Xóa sách khỏi giỏ hàng
```http
DELETE /api/cart/items/1/remove/
```

### 6. Xóa toàn bộ giỏ hàng
```http
DELETE /api/cart/1/clear/
```

---

## 📦 **ORDERS API** - `/api/orders/`

### 1. Tạo đơn hàng từ giỏ hàng
```http
POST /api/orders/create/1/
Content-Type: application/json

{
  "shipping_id": 1,
  "payment_id": 1,
  "staff_id": 1
}
```
**Response:**
```json
{
  "order_id": 1,
  "total_price": 101.98,
  "status": "Pending",
  "message": "Order created successfully"
}
```

### 2. Xem chi tiết đơn hàng
```http
GET /api/orders/1/
```

### 3. Xem đơn hàng của khách hàng
```http
GET /api/orders/customer/1/
```

### 4. Cập nhật trạng thái đơn hàng
```http
PATCH /api/orders/1/status/
Content-Type: application/json

{
  "status": "Confirmed"
}
```
**Trạng thái:** `Pending`, `Confirmed`, `Shipping`, `Delivered`, `Cancelled`

### 5. Lấy danh sách phương thức shipping
```http
GET /api/orders/shipping-methods/
```

### 6. Lấy danh sách phương thức payment
```http
GET /api/orders/payment-methods/
```

### 7. Tạo phương thức shipping
```http
POST /api/orders/shipping-methods/create/
Content-Type: application/json

{
  "method_name": "Express Delivery",
  "fee": 10.0
}
```

### 8. Tạo phương thức payment
```http
POST /api/orders/payment-methods/create/
Content-Type: application/json

{
  "method_name": "Credit Card",
  "status": "Active"
}
```

---

## 👨‍💼 **STAFF API** - `/api/staff/`

### 1. Nhập sách mới vào kho
```http
POST /api/staff/books/add/
Content-Type: application/json

{
  "title": "Design Patterns",
  "author": "Gang of Four",
  "price": 55.99,
  "stock_quantity": 50,
  "category_id": 1
}
```

### 2. Cập nhật số lượng sách trong kho
```http
PUT /api/staff/books/1/stock/
Content-Type: application/json

{
  "stock_quantity": 150
}
```
hoặc
```json
{
  "add_quantity": 50
}
```

### 3. Cập nhật thông tin sách
```http
PUT /api/staff/books/1/update/
Content-Type: application/json

{
  "title": "New Title",
  "price": 49.99,
  "stock_quantity": 200
}
```

### 4. Xóa sách
```http
DELETE /api/staff/books/1/delete/
```

### 5. Lấy danh sách nhân viên
```http
GET /api/staff/
```

---

## 💡 **RECOMMENDATIONS API** - `/api/recommendations/`

### 1. Gợi ý dựa trên lịch sử mua hàng
```http
GET /api/recommendations/by-history/1/
```
**Response:**
```json
[
  {
    "id": 5,
    "title": "Refactoring",
    "author": "Martin Fowler",
    "price": 50.99,
    "category": "Programming",
    "average_rating": 4.7,
    "reason": "Based on your purchase history"
  }
]
```

### 2. Gợi ý sách có rating cao
```http
GET /api/recommendations/by-rating/?limit=10
```

### 3. Gợi ý theo category phổ biến
```http
GET /api/recommendations/by-category/?limit=10
```

### 4. Gợi ý sách tương tự
```http
GET /api/recommendations/similar/1/
```

---

## 🔄 **WORKFLOW SỬ DỤNG HỆ THỐNG**

### **Workflow 1: Khách hàng mua hàng**
```
1. GET /api/books/search/?q=python          → Tìm sách
2. GET /api/books/1/                        → Xem chi tiết sách
3. POST /api/cart/1/add/                    → Thêm vào giỏ hàng
4. GET /api/cart/1/                         → Xem giỏ hàng
5. GET /api/orders/shipping-methods/        → Chọn phương thức ship
6. GET /api/orders/payment-methods/         → Chọn phương thức thanh toán
7. POST /api/orders/create/1/               → Đặt hàng
8. GET /api/orders/customer/1/              → Xem đơn hàng
```

### **Workflow 2: Nhân viên quản lý kho**
```
1. POST /api/staff/books/add/               → Nhập sách mới
2. PUT /api/staff/books/1/stock/            → Cập nhật số lượng
3. GET /api/books/                          → Xem danh sách tồn kho
```

### **Workflow 3: Khách hàng xem gợi ý**
```
1. GET /api/recommendations/by-history/1/   → Gợi ý theo lịch sử
2. GET /api/recommendations/by-rating/      → Gợi ý theo rating
3. GET /api/recommendations/similar/1/      → Gợi ý sách tương tự
```

---

## 📊 **STATUS CODES**

- `200` - OK
- `201` - Created
- `400` - Bad Request
- `404` - Not Found
- `500` - Server Error
