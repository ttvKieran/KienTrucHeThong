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
                'cart_id': None,
                'items': [],
                'total': 0,
                'message': 'No active cart found'
            })
        
        # Lấy các items trong cart
        cart_items = CartItem.objects.filter(cart=cart).select_related('book', 'book__category')
        
        items = [{
            'id': item.id,
            'book_id': item.book.id,
            'book_title': item.book.title,
            'book_price': float(item.book.price),
            'quantity': item.quantity,
            'subtotal': float(item.book.price * item.quantity)
        } for item in cart_items]
        
        total = sum(item['subtotal'] for item in items)
        
        return JsonResponse({
            'cart_id': cart.id,
            'customer_id': customer_id,
            'items': items,
            'total': total
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
def add_to_cart(request, customer_id):
    """Thêm sách vào giỏ hàng"""
    try:
        data = json.loads(request.body)
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
            'cart_id': cart.id,
            'cart_item_id': cart_item.id,
            'book_id': book.id,
            'quantity': cart_item.quantity,
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
def update_cart_item(request, cart_item_id):
    """Cập nhật số lượng sách trong giỏ hàng"""
    try:
        data = json.loads(request.body)
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
            'cart_item_id': cart_item.id,
            'quantity': cart_item.quantity,
            'message': 'Cart item updated successfully'
        })
    except CartItem.DoesNotExist:
        return JsonResponse({'error': 'Cart item not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

# API: Xóa sách khỏi giỏ hàng
@csrf_exempt
@require_http_methods(["DELETE"])
def remove_from_cart(request, cart_item_id):
    """Xóa sách khỏi giỏ hàng"""
    try:
        cart_item = CartItem.objects.get(id=cart_item_id)
        cart_item.delete()
        return JsonResponse({'message': 'Item removed from cart successfully'})
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
