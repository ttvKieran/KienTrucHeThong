"""
Get Book Details Use Case
Business action: Get details of a specific book
"""
from domain.entities import Book
from domain.exceptions import BookNotFoundException
from interfaces.repositories import IBookRepository


class GetBookDetailsUseCase:
    """
    Use case for getting book details
    Pure business logic
    """
    
    def __init__(self, book_repository: IBookRepository):
        self.book_repository = book_repository
    
    def execute(self, book_id: int) -> Book:
        """
        Execute use case to get book details
        
        Args:
            book_id: Book ID
            
        Returns:
            Book entity
            
        Raises:
            BookNotFoundException: If book not found
        """
        book = self.book_repository.get_by_id(book_id)
        
        if book is None:
            raise BookNotFoundException(book_id)
        
        return book
