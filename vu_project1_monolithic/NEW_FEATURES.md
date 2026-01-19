# Tài liệu API - Các chức năng mới

## Tổng quan

Dự án đã được bổ sung các chức năng sau:

1. **Đặt hàng (Order Management)**
2. **Chọn phương thức thanh toán (Payment Methods)**
3. **Chọn phương thức giao hàng (Shipping Methods)**
4. **Gợi ý sách dựa trên lịch sử mua và rating (Book Recommendations)**
5. **Đánh giá sách (Book Ratings)**

## Models mới

### 1. Rating
Lưu trữ đánh giá của khách hàng về sách:
- `customer`: Khách hàng đánh giá
- `book`: Sách được đánh giá
- `score`: Điểm đánh giá (1-5)
- `review`: Nội dung đánh giá (tùy chọn)
- `created_at`, `updated_at`: Thời gian tạo/cập nhật

### 2. Staff
Nhân viên kế thừa từ auth.User:
- `user`: Liên kết với Django User
- `name`: Tên nhân viên
- `role`: Vai trò (manager, sales, warehouse, customer_service)
- `phone`: Số điện thoại
- `hire_date`: Ngày tuyển dụng

### 3. Cart (đã cập nhật)
Thêm thuộc tính:
- `is_active`: Trạng thái giỏ hàng (True/False)

### 4. Order
Đơn hàng của khách hàng:
- `customer`: Khách hàng đặt hàng
- `total_price`: Tổng giá trị đơn hàng
- `status`: Trạng thái (pending, confirmed, processing, shipped, delivered, cancelled)
- `shipping`: Phương thức giao hàng
- `payment`: Phương thức thanh toán
- `shipping_address`: Địa chỉ giao hàng
- `note`: Ghi chú
- `created_at`, `updated_at`: Thời gian tạo/cập nhật

### 5. OrderItem
Chi tiết sản phẩm trong đơn hàng:
- `order`: Đơn hàng
- `book`: Sách
- `quantity`: Số lượng
- `price`: Giá tại thời điểm đặt
- `subtotal`: Tổng tiền (tự động tính)

### 6. Shipping
Phương thức giao hàng:
- `method_name`: Tên phương thức
- `fee`: Phí giao hàng
- `description`: Mô tả
- `estimated_days`: Số ngày dự kiến
- `is_active`: Có hoạt động không

### 7. Payment
Thanh toán:
- `method_name`: Tên phương thức thanh toán
- `status`: Trạng thái (pending, processing, completed, failed, refunded)
- `transaction_id`: Mã giao dịch
- `created_at`, `updated_at`: Thời gian

## API Endpoints

### Đặt hàng (Orders)

#### 1. Lấy danh sách đơn hàng
```
GET /api/orders/
Authorization: Bearer <token>
```

#### 2. Xem chi tiết đơn hàng
```
GET /api/orders/{id}/
Authorization: Bearer <token>
```

#### 3. Tạo đơn hàng từ giỏ hàng
```
POST /api/orders/
Authorization: Bearer <token>

Body:
{
    "shipping_id": 1,
    "payment_method": "Credit Card",
    "shipping_address": "123 Main St, City",
    "note": "Giao hàng buổi sáng",
    "items": [
        {
            "book_id": 1,
            "quantity": 2
        }
    ]
}
```

#### 4. Hủy đơn hàng
```
POST /api/orders/{id}/cancel/
Authorization: Bearer <token>
```

#### 5. Cập nhật trạng thái đơn hàng (Staff only)
```
POST /api/orders/{id}/update_status/
Authorization: Bearer <token>

Body:
{
    "status": "confirmed"
}
```

### Phương thức giao hàng (Shipping)

#### 1. Lấy danh sách phương thức giao hàng
```
GET /api/orders/shipping/
Authorization: Bearer <token>

Response:
[
    {
        "id": 1,
        "method_name": "Standard Shipping",
        "fee": "30000.00",
        "description": "Giao hàng tiêu chuẩn",
        "estimated_days": 3,
        "is_active": true
    }
]
```

### Đánh giá sách (Ratings)

#### 1. Lấy danh sách đánh giá
```
GET /api/ratings/
Authorization: Bearer <token>

Query params:
- book_id: Lọc theo sách
```

#### 2. Tạo/Cập nhật đánh giá
```
POST /api/ratings/
Authorization: Bearer <token>

Body:
{
    "book": 1,
    "score": 5,
    "review": "Sách rất hay!"
}
```

#### 3. Xem đánh giá của tôi
```
GET /api/ratings/my_ratings/
Authorization: Bearer <token>
```

#### 4. Xóa đánh giá
```
DELETE /api/ratings/{id}/
Authorization: Bearer <token>
```

### Gợi ý sách (Recommendations)

#### 1. Gợi ý sách cá nhân hóa
```
GET /api/recommendations/recommendations/
Authorization: Bearer <token>

Query params:
- limit: Số lượng gợi ý (mặc định: 10)

Response:
{
    "recommendations": [...],
    "count": 10
}
```

Thuật toán gợi ý dựa trên:
- Sách của tác giả mà khách hàng đã mua
- Sách có rating cao
- Sách phổ biến (được mua nhiều)

#### 2. Sách thịnh hành
```
GET /api/recommendations/trending/

Query params:
- limit: Số lượng (mặc định: 10)
```

#### 3. Sách tương tự
```
GET /api/recommendations/similar/{book_id}/

Query params:
- limit: Số lượng (mặc định: 5)
```

#### 4. Sách đánh giá cao
```
GET /api/recommendations/highly-rated/

Query params:
- min_rating: Điểm tối thiểu (mặc định: 4.0)
- min_rating_count: Số lượng đánh giá tối thiểu (mặc định: 3)
- limit: Số lượng (mặc định: 10)
```

## Quy trình đặt hàng

1. **Thêm sách vào giỏ hàng**
   ```
   POST /api/cart/add-to-cart/
   ```

2. **Xem giỏ hàng**
   ```
   GET /api/cart/
   ```

3. **Xem các phương thức giao hàng**
   ```
   GET /api/orders/shipping/
   ```

4. **Tạo đơn hàng**
   ```
   POST /api/orders/
   ```
   - Hệ thống tự động:
     - Kiểm tra tồn kho
     - Tính tổng tiền (bao gồm phí ship)
     - Tạo payment record
     - Trừ tồn kho
     - Đánh dấu giỏ hàng là không hoạt động

5. **Theo dõi đơn hàng**
   ```
   GET /api/orders/{id}/
   ```

6. **Hủy đơn hàng (nếu cần)**
   ```
   POST /api/orders/{id}/cancel/
   ```
   - Chỉ hủy được khi status là pending hoặc confirmed
   - Tự động hoàn trả tồn kho

## Quy trình đánh giá sách

1. **Mua sách và hoàn thành đơn hàng**

2. **Tạo đánh giá**
   ```
   POST /api/ratings/
   Body: {"book": 1, "score": 5, "review": "..."}
   ```

3. **Xem đánh giá của mình**
   ```
   GET /api/ratings/my_ratings/
   ```

4. **Nhận gợi ý sách dựa trên lịch sử**
   ```
   GET /api/recommendations/recommendations/
   ```

## Admin Panel

Tất cả models mới đã được thêm vào Django Admin:
- `/admin/bookstore/rating/` - Quản lý đánh giá
- `/admin/bookstore/staff/` - Quản lý nhân viên
- `/admin/bookstore/order/` - Quản lý đơn hàng
- `/admin/bookstore/shipping/` - Quản lý phương thức giao hàng
- `/admin/bookstore/payment/` - Quản lý thanh toán

## Migrate Database

Để áp dụng các thay đổi vào database:

```bash
cd vu_project1_monolithic
python manage.py migrate
```

## Tạo dữ liệu mẫu Shipping

```python
from bookstore.models import Shipping

Shipping.objects.create(
    method_name="Standard Shipping",
    fee=30000,
    description="Giao hàng tiêu chuẩn 3-5 ngày",
    estimated_days=4,
    is_active=True
)

Shipping.objects.create(
    method_name="Express Shipping",
    fee=50000,
    description="Giao hàng nhanh 1-2 ngày",
    estimated_days=1,
    is_active=True
)

Shipping.objects.create(
    method_name="Economy Shipping",
    fee=20000,
    description="Giao hàng tiết kiệm 5-7 ngày",
    estimated_days=6,
    is_active=True
)
```

## Lưu ý

1. **Authentication**: Tất cả endpoints đều yêu cầu authentication
2. **Permissions**: 
   - Customer chỉ xem được đơn hàng của mình
   - Staff có thể xem tất cả đơn hàng và cập nhật trạng thái
3. **Stock Management**: Hệ thống tự động kiểm tra và cập nhật tồn kho khi tạo/hủy đơn hàng
4. **Cart Status**: Giỏ hàng tự động được đánh dấu `is_active=False` sau khi đặt hàng thành công
5. **Rating**: Mỗi customer chỉ có thể đánh giá 1 lần cho 1 cuốn sách (có thể cập nhật)
