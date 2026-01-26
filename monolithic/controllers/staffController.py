from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from store.models import Staff, Book, Category
import json

# API: Lấy danh sách nhân viên
@require_http_methods(["GET"])
def list_staff(request):
    """Lấy danh sách tất cả nhân viên"""
    staff = Staff.objects.all()
    data = [{
        'id': s.id,
        'name': s.name,
        'role': s.role
    } for s in staff]
    return JsonResponse(data, safe=False)

# API: Lấy thông tin một nhân viên
@require_http_methods(["GET"])
def get_staff(request, staff_id):
    """Lấy thông tin một nhân viên"""
    try:
        staff = Staff.objects.get(id=staff_id)
        return JsonResponse({
            'id': staff.id,
            'name': staff.name,
            'role': staff.role
        })
    except Staff.DoesNotExist:
        return JsonResponse({'error': 'Staff not found'}, status=404)

# API: Nhân viên thêm sách mới vào kho
@csrf_exempt
@require_http_methods(["POST"])
def add_book_to_inventory(request):
    """Nhân viên nhập sách mới vào kho"""
    try:
        data = json.loads(request.body)
        
        # Kiểm tra category có tồn tại không
        category = Category.objects.get(id=data['category_id'])
        
        # Tạo sách mới
        book = Book.objects.create(
            title=data['title'],
            author=data['author'],
            price=data['price'],
            stock_quantity=data['stock_quantity'],
            category=category
        )
        
        return JsonResponse({
            'id': book.id,
            'message': 'Book added to inventory successfully',
            'book': {
                'id': book.id,
                'title': book.title,
                'author': book.author,
                'price': float(book.price),
                'stock_quantity': book.stock_quantity,
                'category': category.name
            }
        }, status=201)
    except Category.DoesNotExist:
        return JsonResponse({'error': 'Category not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

# API: Nhân viên cập nhật số lượng sách trong kho
@csrf_exempt
@require_http_methods(["PUT", "PATCH"])
def update_book_stock(request, book_id):
    """Nhân viên cập nhật số lượng sách trong kho"""
    try:
        book = Book.objects.get(id=book_id)
        data = json.loads(request.body)
        
        # Cập nhật stock quantity
        if 'stock_quantity' in data:
            book.stock_quantity = data['stock_quantity']
        
        # Hoặc thêm/bớt số lượng
        if 'add_quantity' in data:
            book.stock_quantity += data['add_quantity']
        
        book.save()
        
        return JsonResponse({
            'id': book.id,
            'title': book.title,
            'stock_quantity': book.stock_quantity,
            'message': 'Stock updated successfully'
        })
    except Book.DoesNotExist:
        return JsonResponse({'error': 'Book not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

# API: Nhân viên cập nhật thông tin sách
@csrf_exempt
@require_http_methods(["PUT", "PATCH"])
def update_book(request, book_id):
    """Nhân viên cập nhật thông tin sách"""
    try:
        book = Book.objects.get(id=book_id)
        data = json.loads(request.body)
        
        if 'title' in data:
            book.title = data['title']
        if 'author' in data:
            book.author = data['author']
        if 'price' in data:
            book.price = data['price']
        if 'stock_quantity' in data:
            book.stock_quantity = data['stock_quantity']
        if 'category_id' in data:
            category = Category.objects.get(id=data['category_id'])
            book.category = category
        
        book.save()
        
        return JsonResponse({
            'id': book.id,
            'message': 'Book updated successfully'
        })
    except Book.DoesNotExist:
        return JsonResponse({'error': 'Book not found'}, status=404)
    except Category.DoesNotExist:
        return JsonResponse({'error': 'Category not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

# API: Nhân viên xóa sách
@csrf_exempt
@require_http_methods(["DELETE"])
def delete_book(request, book_id):
    """Nhân viên xóa sách khỏi kho"""
    try:
        book = Book.objects.get(id=book_id)
        book.delete()
        return JsonResponse({'message': 'Book deleted successfully'})
    except Book.DoesNotExist:
        return JsonResponse({'error': 'Book not found'}, status=404)
