from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q, Avg
from store.models import Book, Category, Rating
from dao.categoryDAO import CategoryDAO
import json

# API: Lấy danh sách tất cả sách
@require_http_methods(["GET"])
def list_books(request):
    """Lấy danh sách tất cả sách"""
    books = Book.objects.select_related('category').all()
    data = [{
        'id': book.id,
        'title': book.title,
        'author': book.author,
        'price': float(book.price),
        'stock_quantity': book.stock_quantity,
        'category_name': book.category.name,
        'category_id': book.category.id
    } for book in books]
    return JsonResponse({'success': True, 'books': data})

# API: Lấy thông tin chi tiết một cuốn sách
@require_http_methods(["GET"])
def get_book(request, book_id):
    """Lấy thông tin chi tiết một cuốn sách"""
    try:
        book = Book.objects.select_related('category').get(id=book_id)
        
        # Tính rating trung bình
        avg_rating = Rating.objects.filter(book=book).aggregate(Avg('score'))['score__avg']
        
        return JsonResponse({
            'success': True,
            'book': {
                'id': book.id,
                'title': book.title,
                'author': book.author,
                'price': float(book.price),
                'stock_quantity': book.stock_quantity,
                'category_name': book.category.name,
                'category_id': book.category.id,
                'average_rating': float(avg_rating) if avg_rating else 0
            }
        })
    except Book.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Book not found'}, status=404)

# API: Tìm kiếm sách theo title, author, category
@require_http_methods(["GET"])
def search_books(request):
    """Tìm kiếm sách theo title, author hoặc category"""
    query = request.GET.get('q', '')
    category_id = request.GET.get('category', None)
    
    books = Book.objects.select_related('category').all()
    
    if query:
        books = books.filter(
            Q(title__icontains=query) | 
            Q(author__icontains=query)
        )
    
    if category_id:
        books = books.filter(category_id=category_id)
    
    data = [{
        'id': book.id,
        'title': book.title,
        'author': book.author,
        'price': float(book.price),
        'stock_quantity': book.stock_quantity,
        'category_name': book.category.name,
        'category_id': book.category.id
    } for book in books]
    
    return JsonResponse({'success': True, 'books': data})

# API: Lấy danh sách categories
@require_http_methods(["GET"])
def list_categories(request):
    """
    Lấy danh sách tất cả categories
    
    Trực tiếp dùng ORM:
    categories = Category.objects.all()
    
    Sử dụng DAO Pattern:
    categories = CategoryDAO.get_all_categories() 
    """
    categories = CategoryDAO.get_all_categories()
    
    data = [{
        'id': cat.id,
        'name': cat.name,
        'description': cat.description
    } for cat in categories]
    
    return JsonResponse({'success': True, 'categories': data})

# API: Thêm rating cho sách
@csrf_exempt
@require_http_methods(["POST"])
def add_rating(request, book_id):
    """Khách hàng đánh giá sách"""
    try:
        data = json.loads(request.body)
        book = Book.objects.get(id=book_id)
        
        rating = Rating.objects.create(
            score=data['score'],
            book=book,
            customer_id=data['customer_id']
        )
        
        return JsonResponse({
            'id': rating.id,
            'message': 'Rating added successfully'
        }, status=201)
    except Book.DoesNotExist:
        return JsonResponse({'error': 'Book not found'}, status=404)

# ==================== STAFF BOOK MANAGEMENT APIs ====================

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
            'success': True,
            'book': {
                'id': book.id,
                'title': book.title,
                'author': book.author,
                'price': float(book.price),
                'stock_quantity': book.stock_quantity,
                'category': category.name
            },
            'message': 'Book added to inventory successfully'
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
            'success': True,
            'book': {
                'id': book.id,
                'title': book.title,
                'stock_quantity': book.stock_quantity
            },
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
            'success': True,
            'book': {'id': book.id},
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
        return JsonResponse({'success': True, 'message': 'Book deleted successfully'})
    except Book.DoesNotExist:
        return JsonResponse({'error': 'Book not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

# API: Lấy ratings của một cuốn sách
@require_http_methods(["GET"])
def get_book_ratings(request, book_id):
    """Lấy tất cả ratings của một cuốn sách"""
    try:
        book = Book.objects.get(id=book_id)
        ratings = Rating.objects.filter(book=book).select_related('customer')
        
        data = [{
            'id': r.id,
            'score': float(r.score),
            'customer_name': r.customer.name
        } for r in ratings]
        
        avg_score = Rating.objects.filter(book=book).aggregate(Avg('score'))['score__avg']
        
        return JsonResponse({
            'book_id': book_id,
            'average_rating': float(avg_score) if avg_score else 0,
            'total_ratings': len(data),
            'ratings': data
        })
    except Book.DoesNotExist:
        return JsonResponse({'error': 'Book not found'}, status=404)
    
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.db.models import Count, Q, Avg
from store.models import Book, Order, OrderItem, Rating, Category
import json

# API: Gợi ý sách dựa trên lịch sử mua hàng
@require_http_methods(["GET"])
def recommend_books_by_history(request, customer_id):
    """Gợi ý sách dựa trên lịch sử mua hàng của khách hàng"""
    try:
        # Lấy các categories mà customer đã mua
        purchased_categories = Category.objects.filter(
            book__orderitem__order__customer_id=customer_id
        ).distinct()
        
        # Lấy các sách đã mua
        purchased_books = Book.objects.filter(
            orderitem__order__customer_id=customer_id
        ).values_list('id', flat=True)
        
        # Gợi ý sách cùng category nhưng chưa mua
        recommended_books = Book.objects.filter(
            category__in=purchased_categories
        ).exclude(
            id__in=purchased_books
        ).select_related('category').annotate(
            avg_rating=Avg('rating__score')
        ).order_by('-avg_rating')[:10]
        
        data = [{
            'id': book.id,
            'title': book.title,
            'author': book.author,
            'price': float(book.price),
            'category_name': book.category.name,
            'average_rating': float(book.avg_rating) if book.avg_rating else 0,
            'reason': 'Based on your purchase history'
        } for book in recommended_books]
        
        return JsonResponse({'success': True, 'recommendations': data})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)

# API: Gợi ý sách dựa trên rating cao
@require_http_methods(["GET"])
def recommend_books_by_rating(request):
    """Gợi ý sách có rating cao nhất"""
    try:
        limit = int(request.GET.get('limit', 10))
        
        # Lấy sách có rating cao nhất
        books = Book.objects.annotate(
            avg_rating=Avg('rating__score'),
            rating_count=Count('rating')
        ).filter(
            rating_count__gt=0  # Chỉ lấy sách có ít nhất 1 rating
        ).select_related('category').order_by('-avg_rating')[:limit]
        
        data = [{
            'id': book.id,
            'title': book.title,
            'author': book.author,
            'price': float(book.price),
            'stock_quantity': book.stock_quantity,
            'category_name': book.category.name,
            'average_rating': float(book.avg_rating) if book.avg_rating else 0,
            'total_ratings': book.rating_count
        } for book in books]
        
        return JsonResponse({'success': True, 'top_rated': data})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)

# API: Gợi ý sách dựa trên category phổ biến
@require_http_methods(["GET"])
def recommend_books_by_popular_category(request):
    """Gợi ý sách từ category phổ biến nhất"""
    try:
        limit = int(request.GET.get('limit', 10))
        
        # Tìm category có nhiều đơn hàng nhất
        popular_categories = Category.objects.annotate(
            order_count=Count('book__orderitem__order', distinct=True)
        ).order_by('-order_count')[:3]
        
        # Convert queryset to list of IDs để tránh lỗi LIMIT trong subquery
        popular_category_ids = list(popular_categories.values_list('id', flat=True))
        
        # Lấy sách từ các category phổ biến
        books = Book.objects.filter(
            category_id__in=popular_category_ids
        ).select_related('category').annotate(
            avg_rating=Avg('rating__score')
        ).order_by('-avg_rating')[:limit]
        
        data = [{
            'id': book.id,
            'title': book.title,
            'author': book.author,
            'price': float(book.price),
            'category_name': book.category.name,
            'average_rating': float(book.avg_rating) if book.avg_rating else 0,
            'reason': 'Popular category'
        } for book in books]
        
        return JsonResponse({'success': True, 'popular_books': data})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)

# API: Gợi ý sách tương tự (cùng author hoặc category)
@require_http_methods(["GET"])
def recommend_similar_books(request, book_id):
    """Gợi ý sách tương tự dựa trên author hoặc category"""
    try:
        book = Book.objects.select_related('category').get(id=book_id)
        
        # Tìm sách cùng author hoặc cùng category
        similar_books = Book.objects.filter(
            Q(author=book.author) | Q(category=book.category)
        ).exclude(
            id=book_id
        ).select_related('category').annotate(
            avg_rating=Avg('rating__score')
        ).order_by('-avg_rating')[:10]
        
        data = [{
            'id': b.id,
            'title': b.title,
            'author': b.author,
            'price': float(b.price),
            'category_name': b.category.name,
            'average_rating': float(b.avg_rating) if b.avg_rating else 0,
            'similarity': 'Same author' if b.author == book.author else 'Same category'
        } for b in similar_books]
        
        return JsonResponse({'success': True, 'similar_books': data})
    except Book.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Book not found'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)
