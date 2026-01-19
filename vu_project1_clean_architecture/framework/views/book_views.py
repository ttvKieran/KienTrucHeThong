"""
Book Views
Framework layer - controllers that handle HTTP requests
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from domain.exceptions import BookNotFoundException
from usecases.book import ListBooksUseCase, GetBookDetailsUseCase
from framework.dependencies import inject_dependencies


@inject_dependencies
class BookListView(APIView):
    """
    Controller for listing books
    Adapter between HTTP and use case
    """
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.list_books_use_case = None  # Will be injected
    
    def get(self, request):
        """
        GET /api/books/
        Query params: search, in_stock
        """
        try:
            search_query = request.query_params.get('search', None)
            in_stock = request.query_params.get('in_stock', 'false').lower() == 'true'
            
            # Execute use case
            books = self.list_books_use_case.execute(
                search_query=search_query,
                in_stock_only=in_stock
            )
            
            # Convert entities to response format
            from framework.serializers import BookSerializer
            serializer = BookSerializer(books, many=True)
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


@inject_dependencies
class BookDetailView(APIView):
    """
    Controller for getting book details
    """
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.get_book_details_use_case = None  # Will be injected
    
    def get(self, request, book_id):
        """GET /api/books/<id>/"""
        try:
            # Execute use case
            book = self.get_book_details_use_case.execute(book_id)
            
            # Convert entity to response format
            from framework.serializers import BookSerializer
            serializer = BookSerializer(book)
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except BookNotFoundException as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
