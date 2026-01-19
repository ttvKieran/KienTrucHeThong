from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from store.serializers import BookSerializer
from store.services.book_service import BookService


@api_view(['GET'])
@permission_classes([AllowAny])
def list_books(request):
    """
    API endpoint to view book catalog
    GET /api/books
    """
    # Get query parameters
    search = request.query_params.get('search', None)
    in_stock = request.query_params.get('in_stock', None)
    in_stock_bool = in_stock and in_stock.lower() == 'true'
    
    # Use service layer for business logic
    books = BookService.get_books_with_filters(search=search, in_stock=in_stock_bool)
    
    serializer = BookSerializer(books, many=True)
    return Response({
        'count': books.count(),
        'books': serializer.data
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_book_detail(request, book_id):
    """
    API endpoint to get book detail
    GET /api/books/<book_id>
    """
    try:
        # Use service layer to get book
        book = BookService.get_book_by_id(book_id)
        serializer = BookSerializer(book)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception:
        return Response({
            'error': 'Book not found'
        }, status=status.HTTP_404_NOT_FOUND)
