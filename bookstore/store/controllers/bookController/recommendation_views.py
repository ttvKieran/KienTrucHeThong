from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from store.models import Book
from store.serializers import BookSerializer
from store.services.recommendation_service import RecommendationService


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_recommendations(request):
    """
    Get personalized book recommendations for the current customer
    """
    try:
        customer = request.user.customer
        limit = int(request.query_params.get('limit', 10))
        
        recommendations = RecommendationService.get_recommendations_for_customer(
            customer=customer,
            limit=limit
        )
        
        serializer = BookSerializer(recommendations, many=True)
        return Response({
            'recommendations': serializer.data,
            'count': len(serializer.data)
        })
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=400
        )


@api_view(['GET'])
def get_trending_books(request):
    """
    Get trending books based on orders and ratings
    """
    limit = int(request.query_params.get('limit', 10))
    trending = RecommendationService.get_trending_books(limit=limit)
    serializer = BookSerializer(trending, many=True)
    
    return Response({
        'trending': serializer.data,
        'count': len(serializer.data)
    })


@api_view(['GET'])
def get_similar_books(request, book_id):
    """
    Get similar books by the same author
    """
    try:
        book = Book.objects.get(id=book_id)
        limit = int(request.query_params.get('limit', 5))
        
        similar = RecommendationService.get_similar_books_by_author(book, limit=limit)
        serializer = BookSerializer(similar, many=True)
        
        return Response({
            'similar_books': serializer.data,
            'count': len(serializer.data)
        })
    except Book.DoesNotExist:
        return Response(
            {'error': 'Book not found'},
            status=404
        )


@api_view(['GET'])
def get_highly_rated_books(request):
    """
    Get highly rated books
    """
    min_rating = float(request.query_params.get('min_rating', 4.0))
    min_rating_count = int(request.query_params.get('min_rating_count', 3))
    limit = int(request.query_params.get('limit', 10))
    
    highly_rated = RecommendationService.get_highly_rated_books(
        min_rating=min_rating,
        min_rating_count=min_rating_count,
        limit=limit
    )
    
    serializer = BookSerializer(highly_rated, many=True)
    
    return Response({
        'highly_rated': serializer.data,
        'count': len(serializer.data)
    })
