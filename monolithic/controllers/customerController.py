from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from store.models import Customer, Address
import json

# API: Lấy danh sách khách hàng
@require_http_methods(["GET"])
def list_customers(request):
    """Lấy danh sách tất cả khách hàng"""
    customers = Customer.objects.select_related('address').all()
    data = [{
        'id': c.id,
        'name': c.name,
        'email': c.email,
        'address': str(c.address)
    } for c in customers]
    return JsonResponse(data, safe=False)

# API: Lấy thông tin một khách hàng
@require_http_methods(["GET"])
def get_customer(request, customer_id):
    """Lấy thông tin chi tiết một khách hàng"""
    try:
        customer = Customer.objects.select_related('address').get(id=customer_id)
        return JsonResponse({
            'id': customer.id,
            'name': customer.name,
            'email': customer.email,
            'address': {
                'id': customer.address.id,
                'house_number': customer.address.house_number,
                'building': customer.address.building,
                'street': customer.address.street,
                'province': customer.address.province
            }
        })
    except Customer.DoesNotExist:
        return JsonResponse({'error': 'Customer not found'}, status=404)

# API: Đăng ký khách hàng mới
@csrf_exempt
@require_http_methods(["POST"])
def register_customer(request):
    """Đăng ký khách hàng mới"""
    try:
        data = json.loads(request.body)
        
        # Tạo address
        address = Address.objects.create(
            house_number=data['address']['house_number'],
            building=data['address'].get('building', ''),
            street=data['address']['street'],
            province=data['address']['province']
        )
        
        # Tạo customer
        customer = Customer.objects.create(
            name=data['name'],
            email=data['email'],
            password=data['password'],  # Nên hash password trong thực tế
            address=address
        )
        
        return JsonResponse({
            'success': True,
            'customer': {
                'id': customer.id,
                'name': customer.name,
                'email': customer.email
            },
            'message': 'Customer registered successfully'
        }, status=201)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

# API: Cập nhật thông tin khách hàng
@csrf_exempt
@require_http_methods(["PUT", "PATCH"])
def update_customer(request, customer_id):
    """Cập nhật thông tin khách hàng"""
    try:
        customer = Customer.objects.get(id=customer_id)
        data = json.loads(request.body)
        
        if 'name' in data:
            customer.name = data['name']
        if 'email' in data:
            customer.email = data['email']
        if 'password' in data:
            customer.password = data['password']
        
        customer.save()
        
        return JsonResponse({
            'id': customer.id,
            'message': 'Customer updated successfully'
        })
    except Customer.DoesNotExist:
        return JsonResponse({'error': 'Customer not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


# API: Login
@csrf_exempt
@require_http_methods(["POST"])
def login_api(request):
    """API đăng nhập cho customer hoặc staff"""
    try:
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')
        user_type = data.get('user_type', 'customer')
        
        if user_type == 'customer':
            try:
                user = Customer.objects.get(email=email, password=password)
                return JsonResponse({
                    'success': True,
                    'user': {
                        'id': user.id,
                        'name': user.name,
                        'email': user.email,
                        'type': 'customer'
                    }
                })
            except Customer.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'Email hoặc mật khẩu không đúng!'}, status=401)
        else:
            from store.models.staff import Staff
            try:
                user = Staff.objects.get(email=email, password=password)
                return JsonResponse({
                    'success': True,
                    'user': {
                        'id': user.id,
                        'name': user.name,
                        'email': user.email,
                        'role': user.role,
                        'type': 'staff'
                    }
                })
            except Staff.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'Thông tin đăng nhập không đúng!'}, status=401)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


# API: Logout
@csrf_exempt
@require_http_methods(["POST"])
def logout_api(request):
    """API đăng xuất"""
    return JsonResponse({'success': True, 'message': 'Đã đăng xuất!'})

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from store.models import Cart, CartItem, Book, Customer
import json
# API: Lấy giỏ hàng hiện tại của khách hàng
@require_http_methods(["GET"])
def get_cart(request, customer_id):
    """Lấy giỏ hàng active của khách hàng"""
    try:
        # Lấy cart active của customer
        cart = Cart.objects.filter(customer_id=customer_id, is_active=True).first()
        
        if not cart:
            return JsonResponse({
                'success': True,
                'cart': {
                    'id': None,
                    'customer_id': customer_id,
                    'items': [],
                    'total': 0
                },
                'message': 'No active cart found'
            })
        
        # Lấy các items trong cart
        cart_items = CartItem.objects.filter(cart=cart).select_related('book', 'book__category')
        
        items = [{
            'id': item.id,
            'book_id': item.book.id,
            'book_title': item.book.title,
            'book_price': float(item.book.price),
            'book_stock': item.book.stock_quantity,
            'quantity': item.quantity,
            'subtotal': float(item.book.price * item.quantity)
        } for item in cart_items]
        
        total = sum(item['subtotal'] for item in items)
        
        return JsonResponse({
            'success': True,
            'cart': {
                'id': cart.id,
                'customer_id': customer_id,
                'items': items,
                'total': total
            }
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

# API: Tạo giỏ hàng mới cho khách hàng
@csrf_exempt
@require_http_methods(["POST"])
def create_cart(request, customer_id):
    """Tạo giỏ hàng mới cho khách hàng"""
    try:
        customer = Customer.objects.get(id=customer_id)
        
        # Deactivate các cart cũ
        Cart.objects.filter(customer=customer, is_active=True).update(is_active=False)
        
        # Tạo cart mới
        cart = Cart.objects.create(
            customer=customer,
            is_active=True
        )
        
        return JsonResponse({
            'cart_id': cart.id,
            'customer_id': customer_id,
            'message': 'Cart created successfully'
        }, status=201)
    except Customer.DoesNotExist:
        return JsonResponse({'error': 'Customer not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

# API: Thêm sách vào giỏ hàng
@csrf_exempt
@require_http_methods(["POST"])
def add_to_cart(request):
    """Thêm sách vào giỏ hàng"""
    try:
        data = json.loads(request.body)
        customer_id = data.get('customer_id')
        customer = Customer.objects.get(id=customer_id)
        book = Book.objects.get(id=data['book_id'])
        quantity = data.get('quantity', 1)
        
        # Kiểm tra stock
        if book.stock_quantity < quantity:
            return JsonResponse({
                'error': 'Not enough stock',
                'available': book.stock_quantity
            }, status=400)
        
        # Lấy hoặc tạo cart active
        cart, created = Cart.objects.get_or_create(
            customer=customer,
            is_active=True
        )
        
        # Kiểm tra xem sách đã có trong cart chưa
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            book=book,
            defaults={'quantity': quantity}
        )
        
        if not created:
            # Nếu đã có, cộng thêm quantity
            cart_item.quantity += quantity
            
            # Kiểm tra stock lại
            if book.stock_quantity < cart_item.quantity:
                return JsonResponse({
                    'error': 'Not enough stock',
                    'available': book.stock_quantity,
                    'current_in_cart': cart_item.quantity - quantity
                }, status=400)
            
            cart_item.save()
        
        return JsonResponse({
            'success': True,
            'cart_item': {
                'id': cart_item.id,
                'cart_id': cart.id,
                'book_id': book.id,
                'quantity': cart_item.quantity
            },
            'message': 'Book added to cart successfully'
        }, status=201 if created else 200)
    except Customer.DoesNotExist:
        return JsonResponse({'error': 'Customer not found'}, status=404)
    except Book.DoesNotExist:
        return JsonResponse({'error': 'Book not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

# API: Cập nhật số lượng sách trong giỏ hàng
@csrf_exempt
@require_http_methods(["PUT", "PATCH"])
def update_cart_item(request):
    """Cập nhật số lượng sách trong giỏ hàng"""
    try:
        data = json.loads(request.body)
        cart_item_id = data.get('item_id')
        cart_item = CartItem.objects.get(id=cart_item_id)
        
        new_quantity = data['quantity']
        
        # Kiểm tra stock
        if cart_item.book.stock_quantity < new_quantity:
            return JsonResponse({
                'error': 'Not enough stock',
                'available': cart_item.book.stock_quantity
            }, status=400)
        
        cart_item.quantity = new_quantity
        cart_item.save()
        
        return JsonResponse({
            'success': True,
            'cart_item': {
                'id': cart_item.id,
                'quantity': cart_item.quantity
            },
            'message': 'Cart item updated successfully'
        })
    except CartItem.DoesNotExist:
        return JsonResponse({'error': 'Cart item not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

# API: Xóa sách khỏi giỏ hàng
@csrf_exempt
@require_http_methods(["DELETE"])
def remove_from_cart(request):
    """Xóa sách khỏi giỏ hàng"""
    try:
        data = json.loads(request.body)
        cart_item_id = data.get('item_id')
        cart_item = CartItem.objects.get(id=cart_item_id)
        cart_item.delete()
        return JsonResponse({'success': True, 'message': 'Item removed from cart successfully'})
    except CartItem.DoesNotExist:
        return JsonResponse({'error': 'Cart item not found'}, status=404)

# API: Xóa toàn bộ giỏ hàng
@csrf_exempt
@require_http_methods(["DELETE"])
def clear_cart(request, customer_id):
    """Xóa toàn bộ giỏ hàng của khách hàng"""
    try:
        cart = Cart.objects.get(customer_id=customer_id, is_active=True)
        CartItem.objects.filter(cart=cart).delete()
        return JsonResponse({'message': 'Cart cleared successfully'})
    except Cart.DoesNotExist:
        return JsonResponse({'error': 'Active cart not found'}, status=404)

