"""
Book Service - Business Logic Layer
Handles book catalog operations
"""
from django.db.models import Q
from store.models import Book


class BookService:
    """Service class for book operations"""
    
    @staticmethod
    def get_all_books():
        """
        Get all books from database
        
        Returns:
            QuerySet: All books
        """
        return Book.objects.all()
    
    @staticmethod
    def search_books(search_query):
        """
        Search books by title or author
        
        Args:
            search_query: Search string
            
        Returns:
            QuerySet: Filtered books
        """
        return Book.objects.filter(
            Q(title__icontains=search_query) | Q(author__icontains=search_query)
        )
    
    @staticmethod
    def filter_books_in_stock(books_queryset):
        """
        Filter books that are in stock
        
        Args:
            books_queryset: QuerySet of books
            
        Returns:
            QuerySet: Books with stock > 0
        """
        return books_queryset.filter(stock__gt=0)
    
    @staticmethod
    def get_books_with_filters(search=None, in_stock=False):
        """
        Get books with optional filters
        
        Args:
            search: Optional search query
            in_stock: Filter only in-stock books
            
        Returns:
            QuerySet: Filtered books
        """
        books = Book.objects.all()
        
        if search:
            books = books.filter(
                Q(title__icontains=search) | Q(author__icontains=search)
            )
        
        if in_stock:
            books = books.filter(stock__gt=0)
        
        return books
    
    @staticmethod
    def get_book_by_id(book_id):
        """
        Get a book by ID
        
        Args:
            book_id: Book ID
            
        Returns:
            Book object
            
        Raises:
            Book.DoesNotExist: If book not found
        """
        return Book.objects.get(id=book_id)
    
    @staticmethod
    def check_book_availability(book, quantity):
        """
        Check if book has enough stock
        
        Args:
            book: Book object
            quantity: Requested quantity
            
        Returns:
            tuple: (is_available: bool, available_stock: int)
        """
        is_available = book.stock >= quantity
        return is_available, book.stock
