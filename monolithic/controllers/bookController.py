from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q, Avg
from store.models import Book, Category, Rating
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
        'category': book.category.name,
        'category_id': book.category.id
    } for book in books]
    return JsonResponse(data, safe=False)

# API: Lấy thông tin chi tiết một cuốn sách
@require_http_methods(["GET"])
def get_book(request, book_id):
    """Lấy thông tin chi tiết một cuốn sách"""
    try:
        book = Book.objects.select_related('category').get(id=book_id)
        
        # Tính rating trung bình
        avg_rating = Rating.objects.filter(book=book).aggregate(Avg('score'))['score__avg']
        
        return JsonResponse({
            'id': book.id,
            'title': book.title,
            'author': book.author,
            'price': float(book.price),
            'stock_quantity': book.stock_quantity,
            'category': book.category.name,
            'category_id': book.category.id,
            'average_rating': float(avg_rating) if avg_rating else 0
        })
    except Book.DoesNotExist:
        return JsonResponse({'error': 'Book not found'}, status=404)

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
        'category': book.category.name,
        'category_id': book.category.id
    } for book in books]
    
    return JsonResponse(data, safe=False)

# API: Lấy danh sách categories
@require_http_methods(["GET"])
def list_categories(request):
    """Lấy danh sách tất cả categories"""
    categories = Category.objects.all()
    data = [{
        'id': cat.id,
        'name': cat.name,
        'description': cat.description
    } for cat in categories]
    return JsonResponse(data, safe=False)

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