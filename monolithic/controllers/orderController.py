from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from store.models import Order, OrderItem, Cart, CartItem, Shipping, Payment, Book
import json
from datetime import datetime

# API: Lấy danh sách tất cả đơn hàng
@require_http_methods(["GET"])
def list_orders(request):
    """Lấy danh sách tất cả đơn hàng"""
    orders = Order.objects.select_related('customer', 'staff', 'shipping', 'payment').all()
    data = [{
        'id': o.id,
        'total_price': float(o.total_price),
        'status': o.status,
        'order_date': str(o.order_date),
        'customer_name': o.customer.name,
        'staff_name': o.staff.name
    } for o in orders]
    return JsonResponse({'success': True, 'orders': data})

# API: Lấy thông tin chi tiết đơn hàng
@require_http_methods(["GET"])
def get_order(request, order_id):
    """Lấy thông tin chi tiết một đơn hàng"""
    try:
        order = Order.objects.select_related('customer', 'staff', 'shipping', 'payment').get(id=order_id)
        order_items = OrderItem.objects.filter(order=order).select_related('book')
        
        items = [{
            'id': item.id,
            'book_id': item.book.id,
            'book_title': item.book.title,
            'quantity': item.quantity,
            'price': float(item.book.price),
            'subtotal': float(item.book.price * item.quantity)
        } for item in order_items]
        
        return JsonResponse({
            'success': True,
            'order': {
                'id': order.id,
                'total_price': float(order.total_price),
                'status': order.status,
                'order_date': str(order.order_date),
                'customer': {
                    'id': order.customer.id,
                    'name': order.customer.name,
                    'email': order.customer.email
                },
                'staff': {
                    'id': order.staff.id,
                    'name': order.staff.name
                },
                'shipping': {
                    'id': order.shipping.id,
                    'method': order.shipping.method_name,
                    'fee': float(order.shipping.fee)
                },
                'payment': {
                    'id': order.payment.id,
                    'method': order.payment.method_name,
                    'status': order.payment.status
                },
                'items': items
            }
        })
    except Order.DoesNotExist:
        return JsonResponse({'error': 'Order not found'}, status=404)

# API: Lấy đơn hàng của khách hàng
@require_http_methods(["GET"])
def get_customer_orders(request, customer_id):
    """Lấy tất cả đơn hàng của một khách hàng"""
    orders = Order.objects.filter(customer_id=customer_id).select_related('shipping', 'payment')
    data = [{
        'id': o.id,
        'total_price': float(o.total_price),
        'status': o.status,
        'order_date': str(o.order_date),
        'shipping_method': o.shipping.method_name,
        'payment_method': o.payment.method_name,
        'payment_status': o.payment.status
    } for o in orders]
    return JsonResponse({'success': True, 'orders': data})

# API: Tạo đơn hàng từ giỏ hàng
@csrf_exempt
@require_http_methods(["POST"])
def create_order_from_cart(request, customer_id):
    """Khách hàng đặt hàng từ giỏ hàng"""
    try:
        with transaction.atomic():
            data = json.loads(request.body)
            
            # Lấy cart active
            cart = Cart.objects.get(customer_id=customer_id, is_active=True)
            cart_items = CartItem.objects.filter(cart=cart).select_related('book')
            
            if not cart_items:
                return JsonResponse({'error': 'Cart is empty'}, status=400)
            
            # Lấy hoặc tạo shipping method
            shipping_id = data.get('shipping_id')
            shipping = Shipping.objects.get(id=shipping_id)
            
            # Lấy hoặc tạo payment method
            payment_id = data.get('payment_id')
            payment = Payment.objects.get(id=payment_id)
            
            # Tính tổng giá
            total_price = sum(item.book.price * item.quantity for item in cart_items)
            total_price += shipping.fee  # Bây giờ cả 2 đều là Decimal
            
            # Lấy staff (mặc định lấy staff đầu tiên, hoặc từ request)
            staff_id = data.get('staff_id', 1)
            
            # Tạo order
            order = Order.objects.create(
                total_price=total_price,
                status='Pending',
                customer_id=customer_id,
                staff_id=staff_id,
                shipping=shipping,
                payment=payment
            )
            
            # Tạo order items và giảm stock
            for cart_item in cart_items:
                # Kiểm tra stock
                if cart_item.book.stock_quantity < cart_item.quantity:
                    raise Exception(f'Not enough stock for {cart_item.book.title}')
                
                # Tạo order item
                OrderItem.objects.create(
                    order=order,
                    book=cart_item.book,
                    quantity=cart_item.quantity
                )
                
                # Giảm stock
                cart_item.book.stock_quantity -= cart_item.quantity
                cart_item.book.save()
            
            # Xóa cart items và deactivate cart
            cart_items.delete()
            cart.is_active = False
            cart.save()
            
            return JsonResponse({
                'success': True,
                'order': {
                    'id': order.id,
                    'total_price': float(total_price),
                    'status': order.status
                },
                'message': 'Order created successfully'
            }, status=201)
            
    except Cart.DoesNotExist:
        return JsonResponse({'error': 'Active cart not found'}, status=404)
    except Shipping.DoesNotExist:
        return JsonResponse({'error': 'Shipping method not found'}, status=404)
    except Payment.DoesNotExist:
        return JsonResponse({'error': 'Payment method not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

# API: Cập nhật trạng thái đơn hàng
@csrf_exempt
@require_http_methods(["PATCH"])
def update_order_status(request, order_id):
    """Nhân viên cập nhật trạng thái đơn hàng"""
    try:
        order = Order.objects.get(id=order_id)
        data = json.loads(request.body)
        
        if 'status' in data:
            order.status = data['status']
            order.save()
        
        return JsonResponse({
            'success': True,
            'order': {
                'id': order.id,
                'status': order.status
            },
            'message': 'Order status updated successfully'
        })
    except Order.DoesNotExist:
        return JsonResponse({'error': 'Order not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

# API: Lấy danh sách phương thức shipping
@require_http_methods(["GET"])
def list_shipping_methods(request):
    """Lấy danh sách phương thức giao hàng"""
    methods = Shipping.objects.all()
    data = [{
        'id': m.id,
        'method_name': m.method_name,
        'fee': float(m.fee)
    } for m in methods]
    return JsonResponse({'success': True, 'shipping_methods': data})

# API: Lấy danh sách phương thức payment
@require_http_methods(["GET"])
def list_payment_methods(request):
    """Lấy danh sách phương thức thanh toán"""
    methods = Payment.objects.all()
    data = [{
        'id': m.id,
        'method_name': m.method_name,
        'status': m.status
    } for m in methods]
    return JsonResponse({'success': True, 'payment_methods': data})

# API: Tạo phương thức shipping mới
@csrf_exempt
@require_http_methods(["POST"])
def create_shipping_method(request):
    """Tạo phương thức giao hàng mới"""
    try:
        data = json.loads(request.body)
        shipping = Shipping.objects.create(
            method_name=data['method_name'],
            fee=data['fee']
        )
        return JsonResponse({
            'id': shipping.id,
            'message': 'Shipping method created successfully'
        }, status=201)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

# API: Tạo phương thức payment mới
@csrf_exempt
@require_http_methods(["POST"])
def create_payment_method(request):
    """Tạo phương thức thanh toán mới"""
    try:
        data = json.loads(request.body)
        payment = Payment.objects.create(
            method_name=data['method_name'],
            status=data.get('status', 'Active')
        )
        return JsonResponse({
            'id': payment.id,
            'message': 'Payment method created successfully'
        }, status=201)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
