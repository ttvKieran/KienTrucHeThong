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
            'category': book.category.name,
            'average_rating': float(book.avg_rating) if book.avg_rating else 0,
            'reason': 'Based on your purchase history'
        } for book in recommended_books]
        
        return JsonResponse(data, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

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
            'category': book.category.name,
            'average_rating': float(book.avg_rating) if book.avg_rating else 0,
            'total_ratings': book.rating_count
        } for book in books]
        
        return JsonResponse(data, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

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
            'category': book.category.name,
            'average_rating': float(book.avg_rating) if book.avg_rating else 0,
            'reason': 'Popular category'
        } for book in books]
        
        return JsonResponse(data, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

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
            'category': b.category.name,
            'average_rating': float(b.avg_rating) if b.avg_rating else 0,
            'similarity': 'Same author' if b.author == book.author else 'Same category'
        } for b in similar_books]
        
        return JsonResponse(data, safe=False)
    except Book.DoesNotExist:
        return JsonResponse({'error': 'Book not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
