"""
Book Repository Implementation
Infrastructure layer - implements repository interface using Django ORM
"""
from typing import List, Optional
from django.db.models import Q
from domain.entities import Book
from domain.value_objects import SearchCriteria
from interfaces.repositories import IBookRepository
from infrastructure.models import BookModel


class DjangoBookRepository(IBookRepository):
    """
    Django ORM implementation of Book repository
    """
    
    def _to_entity(self, model: BookModel) -> Book:
        """Convert Django model to domain entity"""
        return Book(
            id=model.id,
            title=model.title,
            author=model.author,
            stock=model.stock,
            note=model.note,
            slug=model.slug
        )
    
    def _to_model(self, entity: Book, model: BookModel = None) -> BookModel:
        """Convert domain entity to Django model"""
        if model is None:
            model = BookModel()
        
        model.title = entity.title
        model.author = entity.author
        model.stock = entity.stock
        model.note = entity.note
        model.slug = entity.slug
        
        return model
    
    def get_all(self) -> List[Book]:
        """Get all books"""
        models = BookModel.objects.all()
        return [self._to_entity(model) for model in models]
    
    def get_by_id(self, book_id: int) -> Optional[Book]:
        """Get book by ID"""
        try:
            model = BookModel.objects.get(id=book_id)
            return self._to_entity(model)
        except BookModel.DoesNotExist:
            return None
    
    def search(self, criteria: SearchCriteria) -> List[Book]:
        """Search books based on criteria"""
        queryset = BookModel.objects.all()
        
        # Apply search query
        if criteria.has_query():
            queryset = queryset.filter(
                Q(title__icontains=criteria.query) | 
                Q(author__icontains=criteria.query)
            )
        
        # Apply stock filter
        if criteria.in_stock_only:
            queryset = queryset.filter(stock__gt=0)
        
        return [self._to_entity(model) for model in queryset]
    
    def save(self, book: Book) -> Book:
        """Save or update book"""
        if book.id:
            # Update existing
            try:
                model = BookModel.objects.get(id=book.id)
                model = self._to_model(book, model)
            except BookModel.DoesNotExist:
                model = self._to_model(book)
        else:
            # Create new
            model = self._to_model(book)
        
        model.save()
        return self._to_entity(model)
    
    def delete(self, book_id: int) -> bool:
        """Delete book by ID"""
        try:
            model = BookModel.objects.get(id=book_id)
            model.delete()
            return True
        except BookModel.DoesNotExist:
            return False
    
    def update_stock(self, book_id: int, quantity_change: int) -> bool:
        """Update book stock"""
        try:
            model = BookModel.objects.get(id=book_id)
            model.stock += quantity_change
            if model.stock < 0:
                return False
            model.save()
            return True
        except BookModel.DoesNotExist:
            return False
