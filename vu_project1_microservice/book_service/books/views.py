"""
Book Service Views
"""
from datetime import datetime
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from django.db.models import Q

from .models import Book
from .serializers import BookSerializer, BookListSerializer, StockUpdateSerializer


@api_view(['GET'])
def health_check(request):
    """Health check endpoint"""
    return Response({
        'status': 'healthy',
        'service': 'book-service',
        'timestamp': datetime.now().isoformat()
    })


class BookListView(APIView):
    """
    List all books or create a new book
    GET /api/books/ - List books with optional search
    POST /api/books/ - Create new book
    """
    
    def get(self, request):
        """List all books with optional search filter"""
        search = request.query_params.get('search', None)
        
        books = Book.objects.all()
        
        if search:
            books = books.filter(
                Q(title__icontains=search) | Q(author__icontains=search)
            )
        
        serializer = BookListSerializer(books, many=True)
        return Response({
            'count': books.count(),
            'books': serializer.data
        })
    
    def post(self, request):
        """Create a new book"""
        serializer = BookSerializer(data=request.data)
        
        if serializer.is_valid():
            book = serializer.save()
            return Response(
                BookSerializer(book).data,
                status=status.HTTP_201_CREATED
            )
        
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class BookDetailView(APIView):
    """
    Retrieve, update, or delete a book
    GET /api/books/{id}/ - Get book details
    PUT /api/books/{id}/ - Update book
    DELETE /api/books/{id}/ - Delete book
    """
    
    def get(self, request, book_id):
        """Get book details by ID"""
        book = get_object_or_404(Book, id=book_id)
        serializer = BookSerializer(book)
        return Response(serializer.data)
    
    def put(self, request, book_id):
        """Update book"""
        book = get_object_or_404(Book, id=book_id)
        serializer = BookSerializer(book, data=request.data, partial=True)
        
        if serializer.is_valid():
            book = serializer.save()
            return Response(BookSerializer(book).data)
        
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    
    def delete(self, request, book_id):
        """Delete book"""
        book = get_object_or_404(Book, id=book_id)
        book.delete()
        return Response(
            {'message': 'Book deleted successfully'},
            status=status.HTTP_204_NO_CONTENT
        )


class BookStockView(APIView):
    """
    Manage book stock
    POST /api/books/{id}/stock/ - Update stock
    """
    
    def post(self, request, book_id):
        """Update book stock (increase or decrease)"""
        book = get_object_or_404(Book, id=book_id)
        serializer = StockUpdateSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        
        quantity = serializer.validated_data['quantity']
        operation = serializer.validated_data['operation']
        
        try:
            if operation == 'increase':
                book.increase_stock(quantity)
                message = f"Stock increased by {quantity}"
            else:  # decrease
                book.reduce_stock(quantity)
                message = f"Stock decreased by {quantity}"
            
            return Response({
                'message': message,
                'book_id': book.id,
                'new_stock': book.stock
            })
            
        except ValueError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class CheckStockView(APIView):
    """
    Check if book has sufficient stock
    POST /api/books/check-stock/ - Check stock availability
    Body: {book_id: int, quantity: int}
    """
    
    def post(self, request):
        """Check if book has sufficient stock"""
        book_id = request.data.get('book_id')
        quantity = request.data.get('quantity')
        
        if not book_id or not quantity:
            return Response(
                {'error': 'book_id and quantity are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            quantity = int(quantity)
            if quantity <= 0:
                return Response(
                    {'error': 'Quantity must be positive'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except ValueError:
            return Response(
                {'error': 'Invalid quantity'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        book = get_object_or_404(Book, id=book_id)
        
        has_stock = book.has_sufficient_stock(quantity)
        
        return Response({
            'book_id': book.id,
            'title': book.title,
            'price': str(book.price),
            'current_stock': book.stock,
            'requested_quantity': quantity,
            'available': has_stock
        })
