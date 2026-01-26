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
            'id': customer.id,
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
