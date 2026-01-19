"""
List Books Use Case
Business action: Get all books from catalog
"""
from typing import List
from domain.entities import Book
from domain.value_objects import SearchCriteria
from domain.exceptions import BookNotFoundException
from interfaces.repositories import IBookRepository


class ListBooksUseCase:
    """
    Use case for listing books
    Pure business logic
    """
    
    def __init__(self, book_repository: IBookRepository):
        self.book_repository = book_repository
    
    def execute(self, search_query: str = None, in_stock_only: bool = False) -> List[Book]:
        """
        Execute use case to list books
        
        Args:
            search_query: Optional search term
            in_stock_only: Filter only in-stock books
            
        Returns:
            List of books
        """
        criteria = SearchCriteria(query=search_query, in_stock_only=in_stock_only)
        
        if criteria.has_query() or criteria.in_stock_only:
            return self.book_repository.search(criteria)
        
        return self.book_repository.get_all()
