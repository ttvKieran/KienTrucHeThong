from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.db.models import Avg, Count, Q
from store.models import Book, Rating, Order, OrderItem, Category, Customer
import numpy as np
from collections import defaultdict, Counter
import json

def calculate_similarity(ratings1, ratings2, book_ids):
    """
    Tính độ tương đồng cosine giữa 2 user dựa trên ratings
    """
    common_books = set(ratings1.keys()) & set(ratings2.keys()) & book_ids
    
    if len(common_books) == 0:
        return 0
    
    # Vector ratings
    vec1 = np.array([ratings1[book] for book in common_books])
    vec2 = np.array([ratings2[book] for book in common_books])
    
    # Cosine similarity
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)
    
    if norm1 == 0 or norm2 == 0:
        return 0
    
    return np.dot(vec1, vec2) / (norm1 * norm2)


@require_http_methods(["GET"])
def ai_collaborative_filtering(request, customer_id):
    """
    AI Collaborative Filtering: Gợi ý sách dựa trên người dùng tương tự
    Sử dụng User-based Collaborative Filtering với Cosine Similarity
    """
    try:
        limit = int(request.GET.get('limit', 10))
        
        # Lấy tất cả ratings
        all_ratings = Rating.objects.select_related('customer', 'book').all()
        
        # Tạo ma trận user-book ratings
        user_ratings = defaultdict(dict)
        for rating in all_ratings:
            user_ratings[rating.customer_id][rating.book_id] = float(rating.score)
        
        # Kiểm tra user có ratings không
        if customer_id not in user_ratings or len(user_ratings[customer_id]) == 0:
            # Fallback: gợi ý sách rating cao nhất
            return recommend_top_rated_fallback(limit)
        
        # Tìm users tương tự
        target_user_ratings = user_ratings[customer_id]
        all_book_ids = set(target_user_ratings.keys())
        
        similarities = []
        for user_id, ratings in user_ratings.items():
            if user_id != customer_id:
                similarity = calculate_similarity(target_user_ratings, ratings, all_book_ids)
                if similarity > 0:
                    similarities.append((user_id, similarity))
        
        # Sắp xếp theo độ tương đồng
        similarities.sort(key=lambda x: x[1], reverse=True)
        top_similar_users = similarities[:10]  # Top 10 users tương tự
        
        if len(top_similar_users) == 0:
            return recommend_top_rated_fallback(limit)
        
        # Tính điểm predicted cho các sách chưa đọc
        book_scores = defaultdict(float)
        book_weights = defaultdict(float)
        
        read_books = set(target_user_ratings.keys())
        
        for user_id, similarity in top_similar_users:
            for book_id, rating in user_ratings[user_id].items():
                if book_id not in read_books:
                    book_scores[book_id] += similarity * rating
                    book_weights[book_id] += similarity
        
        # Tính điểm trung bình weighted
        recommendations = []
        for book_id, total_score in book_scores.items():
            if book_weights[book_id] > 0:
                predicted_score = total_score / book_weights[book_id]
                recommendations.append((book_id, predicted_score))
        
        # Sắp xếp và lấy top recommendations
        recommendations.sort(key=lambda x: x[1], reverse=True)
        top_book_ids = [book_id for book_id, _ in recommendations[:limit]]
        
        if len(top_book_ids) == 0:
            return recommend_top_rated_fallback(limit)
        
        # Lấy thông tin sách
        books = Book.objects.filter(id__in=top_book_ids).select_related('category').annotate(
            avg_rating=Avg('rating__score'),
            rating_count=Count('rating')
        )
        
        # Tạo dict để giữ thứ tự
        book_dict = {book.id: book for book in books}
        ordered_books = [book_dict[book_id] for book_id in top_book_ids if book_id in book_dict]
        
        data = [{
            'id': book.id,
            'title': book.title,
            'author': book.author,
            'price': float(book.price),
            'stock_quantity': book.stock_quantity,
            'category_name': book.category.name,
            'average_rating': float(book.avg_rating) if book.avg_rating else 0,
            'total_ratings': book.rating_count,
            'reason': 'AI: Users similar to you liked this',
            'algorithm': 'Collaborative Filtering'
        } for book in ordered_books]
        
        return JsonResponse({
            'success': True, 
            'recommendations': data,
            'algorithm': 'AI Collaborative Filtering (User-based)',
            'similar_users_count': len(top_similar_users)
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


@require_http_methods(["GET"])
def ai_content_based_filtering(request, customer_id):
    """
    AI Content-Based Filtering: Gợi ý sách dựa trên nội dung (category, author)
    của những sách user đã đánh giá cao
    """
    try:
        limit = int(request.GET.get('limit', 10))
        
        # Lấy ratings của customer
        user_ratings = Rating.objects.filter(
            customer_id=customer_id
        ).select_related('book', 'book__category').order_by('-score')
        
        if not user_ratings.exists():
            return recommend_top_rated_fallback(limit)
        
        # Phân tích preferences
        liked_books = user_ratings.filter(score__gte=4.0)  # Rating >= 4.0
        
        if not liked_books.exists():
            liked_books = user_ratings[:5]  # Lấy top 5 rated books
        
        # Đếm categories và authors yêu thích
        category_scores = Counter()
        author_scores = Counter()
        rated_book_ids = set()
        
        for rating in liked_books:
            weight = float(rating.score) / 5.0  # Normalize to 0-1
            category_scores[rating.book.category_id] += weight
            author_scores[rating.book.author] += weight
            rated_book_ids.add(rating.book_id)
        
        # Lấy top categories và authors
        top_categories = [cat_id for cat_id, _ in category_scores.most_common(5)]
        top_authors = [author for author, _ in author_scores.most_common(5)]
        
        # Tìm sách tương tự
        similar_books = Book.objects.filter(
            Q(category_id__in=top_categories) | Q(author__in=top_authors)
        ).exclude(
            id__in=rated_book_ids
        ).select_related('category').annotate(
            avg_rating=Avg('rating__score'),
            rating_count=Count('rating')
        )
        
        # Tính điểm cho mỗi sách
        book_scores = []
        for book in similar_books:
            score = 0
            
            # Điểm từ category
            if book.category_id in category_scores:
                score += category_scores[book.category_id] * 2
            
            # Điểm từ author
            if book.author in author_scores:
                score += author_scores[book.author] * 1.5
            
            # Bonus cho sách có rating cao
            if book.avg_rating:
                score += float(book.avg_rating) * 0.3
            
            book_scores.append((book, score))
        
        # Sắp xếp theo điểm
        book_scores.sort(key=lambda x: x[1], reverse=True)
        top_books = [book for book, _ in book_scores[:limit]]
        
        if len(top_books) == 0:
            return recommend_top_rated_fallback(limit)
        
        data = [{
            'id': book.id,
            'title': book.title,
            'author': book.author,
            'price': float(book.price),
            'stock_quantity': book.stock_quantity,
            'category_name': book.category.name,
            'average_rating': float(book.avg_rating) if book.avg_rating else 0,
            'total_ratings': book.rating_count,
            'reason': 'AI: Based on your reading preferences',
            'algorithm': 'Content-Based Filtering'
        } for book in top_books]
        
        return JsonResponse({
            'success': True, 
            'recommendations': data,
            'algorithm': 'AI Content-Based Filtering',
            'top_categories': [Category.objects.get(id=cat_id).name for cat_id in top_categories]
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


@require_http_methods(["GET"])
def ai_hybrid_recommendation(request, customer_id):
    """
    AI Hybrid Recommendation: Kết hợp Collaborative Filtering + Content-Based
    Đây là thuật toán mạnh nhất, kết hợp 2 phương pháp
    """
    try:
        limit = int(request.GET.get('limit', 12))
        
        # Gọi cả 2 algorithms
        cf_response = ai_collaborative_filtering(request, customer_id)
        cb_response = ai_content_based_filtering(request, customer_id)
        
        cf_data = json.loads(cf_response.content)
        cb_data = json.loads(cb_response.content)
        
        # Kết hợp kết quả
        book_scores = {}
        
        # Thêm điểm từ Collaborative Filtering
        if cf_data.get('success') and cf_data.get('recommendations'):
            for i, book in enumerate(cf_data['recommendations']):
                score = (limit - i) * 1.2  # Weight cao hơn cho CF
                book_scores[book['id']] = {
                    'book': book,
                    'score': score
                }
        
        # Thêm điểm từ Content-Based
        if cb_data.get('success') and cb_data.get('recommendations'):
            for i, book in enumerate(cb_data['recommendations']):
                score = (limit - i) * 1.0
                if book['id'] in book_scores:
                    book_scores[book['id']]['score'] += score  # Cộng điểm nếu trùng
                else:
                    book_scores[book['id']] = {
                        'book': book,
                        'score': score
                    }
        
        # Sắp xếp theo điểm tổng hợp
        sorted_books = sorted(
            book_scores.values(),
            key=lambda x: x['score'],
            reverse=True
        )[:limit]
        
        recommendations = []
        for item in sorted_books:
            book = item['book'].copy()
            book['reason'] = 'AI: Hybrid recommendation (Best match)'
            book['algorithm'] = 'Hybrid (CF + CB)'
            recommendations.append(book)
        
        if len(recommendations) == 0:
            return recommend_top_rated_fallback(limit)
        
        return JsonResponse({
            'success': True,
            'recommendations': recommendations,
            'algorithm': 'AI Hybrid Recommendation System',
            'methods': ['Collaborative Filtering', 'Content-Based Filtering']
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


@require_http_methods(["GET"])
def ai_trending_books(request):
    """
    AI Trending: Sách đang trending dựa trên orders gần đây và ratings
    """
    try:
        limit = int(request.GET.get('limit', 10))
        days = int(request.GET.get('days', 30))
        
        from datetime import timedelta, datetime
        
        # Lấy orders trong N ngày gần đây
        cutoff_date = datetime.now().date() - timedelta(days=days)
        
        # Đếm số lượng bán và tính điểm trending
        trending_books = Book.objects.annotate(
            recent_sales=Count(
                'orderitem__order',
                filter=Q(orderitem__order__order_date__gte=cutoff_date)
            ),
            avg_rating=Avg('rating__score'),
            rating_count=Count('rating')
        ).filter(
            recent_sales__gt=0
        ).select_related('category')
        
        # Tính trending score
        book_scores = []
        for book in trending_books:
            # Score = sales * 2 + avg_rating * 0.5 + log(rating_count)
            score = book.recent_sales * 2
            if book.avg_rating:
                score += float(book.avg_rating) * 0.5
            if book.rating_count > 0:
                score += np.log(book.rating_count + 1) * 0.3
            
            book_scores.append((book, score))
        
        # Sắp xếp theo trending score
        book_scores.sort(key=lambda x: x[1], reverse=True)
        top_books = [book for book, _ in book_scores[:limit]]
        
        if len(top_books) == 0:
            return recommend_top_rated_fallback(limit)
        
        data = [{
            'id': book.id,
            'title': book.title,
            'author': book.author,
            'price': float(book.price),
            'stock_quantity': book.stock_quantity,
            'category_name': book.category.name,
            'average_rating': float(book.avg_rating) if book.avg_rating else 0,
            'total_ratings': book.rating_count,
            'recent_sales': book.recent_sales,
            'reason': f'Trending: {book.recent_sales} sales in last {days} days',
            'algorithm': 'AI Trending Analysis'
        } for book in top_books]
        
        return JsonResponse({
            'success': True,
            'trending': data,
            'algorithm': 'AI Trending Analysis',
            'period_days': days
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


@require_http_methods(["GET"])
def ai_personalized_homepage(request, customer_id):
    """
    AI Personalized Homepage: Trang chủ cá nhân hóa với nhiều sections khác nhau
    """
    try:
        # Lấy hybrid recommendations
        hybrid = ai_hybrid_recommendation(request, customer_id)
        hybrid_data = json.loads(hybrid.content)
        
        # Lấy trending books
        trending = ai_trending_books(request)
        trending_data = json.loads(trending.content)
        
        # Lấy sách mới (giả sử dựa trên ID cao nhất)
        new_books = Book.objects.select_related('category').annotate(
            avg_rating=Avg('rating__score'),
            rating_count=Count('rating')
        ).order_by('-id')[:8]
        
        new_books_data = [{
            'id': book.id,
            'title': book.title,
            'author': book.author,
            'price': float(book.price),
            'stock_quantity': book.stock_quantity,
            'category_name': book.category.name,
            'average_rating': float(book.avg_rating) if book.avg_rating else 0,
            'total_ratings': book.rating_count,
            'reason': 'New arrival',
            'algorithm': 'Recently added'
        } for book in new_books]
        
        return JsonResponse({
            'success': True,
            'sections': {
                'for_you': hybrid_data.get('recommendations', [])[:6],
                'trending': trending_data.get('trending', [])[:6],
                'new_arrivals': new_books_data[:6]
            },
            'algorithm': 'AI Personalized Homepage'
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


# Helper function: Fallback khi không đủ dữ liệu
def recommend_top_rated_fallback(limit=10):
    """
    Fallback: Gợi ý sách rating cao nhất khi không đủ dữ liệu cho AI
    """
    books = Book.objects.annotate(
        avg_rating=Avg('rating__score'),
        rating_count=Count('rating')
    ).filter(
        rating_count__gt=0
    ).select_related('category').order_by('-avg_rating')[:limit]
    
    data = [{
        'id': book.id,
        'title': book.title,
        'author': book.author,
        'price': float(book.price),
        'stock_quantity': book.stock_quantity,
        'category_name': book.category.name,
        'average_rating': float(book.avg_rating) if book.avg_rating else 0,
        'total_ratings': book.rating_count,
        'reason': 'Top rated books',
        'algorithm': 'Fallback: Rating-based'
    } for book in books]
    
    if len(data) == 0:
        # Nếu không có rating nào, lấy random books
        books = Book.objects.select_related('category').all()[:limit]
        data = [{
            'id': book.id,
            'title': book.title,
            'author': book.author,
            'price': float(book.price),
            'stock_quantity': book.stock_quantity,
            'category_name': book.category.name,
            'average_rating': 0,
            'total_ratings': 0,
            'reason': 'Popular books',
            'algorithm': 'Fallback: Random selection'
        } for book in books]
    
    return JsonResponse({'success': True, 'recommendations': data})
