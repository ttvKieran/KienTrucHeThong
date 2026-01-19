from django.db import models
from django.db.models import Count, Avg, Q
from store.models import Book, Rating, Order, OrderItem, Customer


class RecommendationService:
    """
    Service class for book recommendation system
    """
    
    @staticmethod
    def get_recommendations_for_customer(customer, limit=10):
        """
        Get book recommendations for a customer based on:
        1. Purchase history (books from same authors)
        2. High-rated books
        3. Popular books (most purchased)
        
        Args:
            customer: Customer instance
            limit: Maximum number of recommendations
            
        Returns:
            QuerySet of recommended books
        """
        # Get books the customer has already purchased
        purchased_books = OrderItem.objects.filter(
            order__customer=customer
        ).values_list('book_id', flat=True).distinct()
        
        # Get authors from customer's purchase history
        purchased_authors = Book.objects.filter(
            id__in=purchased_books
        ).values_list('author', flat=True).distinct()
        
        # Recommendation strategy:
        # 1. Books by same authors (not already purchased)
        same_author_books = Book.objects.filter(
            author__in=purchased_authors
        ).exclude(
            id__in=purchased_books
        ).annotate(
            avg_rating=Avg('ratings__score')
        )
        
        # 2. High-rated books (not already purchased)
        high_rated_books = Book.objects.exclude(
            id__in=purchased_books
        ).annotate(
            avg_rating=Avg('ratings__score'),
            rating_count=Count('ratings')
        ).filter(
            rating_count__gte=3  # At least 3 ratings
        ).order_by('-avg_rating')
        
        # 3. Popular books (most purchased, not already purchased)
        popular_books = Book.objects.exclude(
            id__in=purchased_books
        ).annotate(
            order_count=Count('orderitem')
        ).filter(
            order_count__gte=1
        ).order_by('-order_count')
        
        # Combine recommendations (prioritize same author, then rating, then popularity)
        recommended_ids = []
        
        # Add same author books
        for book in same_author_books[:limit//2]:
            if book.id not in recommended_ids:
                recommended_ids.append(book.id)
        
        # Add high-rated books
        for book in high_rated_books[:limit]:
            if book.id not in recommended_ids and len(recommended_ids) < limit:
                recommended_ids.append(book.id)
        
        # Add popular books if still need more
        for book in popular_books[:limit]:
            if book.id not in recommended_ids and len(recommended_ids) < limit:
                recommended_ids.append(book.id)
        
        # Return books maintaining the order
        recommended_books = Book.objects.filter(id__in=recommended_ids)
        
        # Preserve order
        id_to_book = {book.id: book for book in recommended_books}
        ordered_books = [id_to_book[book_id] for book_id in recommended_ids if book_id in id_to_book]
        
        return ordered_books
    
    @staticmethod
    def get_trending_books(limit=10):
        """
        Get trending books based on recent orders and high ratings
        """
        trending = Book.objects.annotate(
            avg_rating=Avg('ratings__score'),
            rating_count=Count('ratings'),
            order_count=Count('orderitem')
        ).filter(
            Q(rating_count__gte=1) | Q(order_count__gte=1)
        ).order_by('-order_count', '-avg_rating')[:limit]
        
        return trending
    
    @staticmethod
    def get_similar_books_by_author(book, limit=5):
        """
        Get similar books by the same author
        """
        similar = Book.objects.filter(
            author=book.author
        ).exclude(
            id=book.id
        ).annotate(
            avg_rating=Avg('ratings__score')
        ).order_by('-avg_rating')[:limit]
        
        return similar
    
    @staticmethod
    def get_highly_rated_books(min_rating=4.0, min_rating_count=3, limit=10):
        """
        Get highly rated books
        
        Args:
            min_rating: Minimum average rating
            min_rating_count: Minimum number of ratings
            limit: Maximum number of books
        """
        highly_rated = Book.objects.annotate(
            avg_rating=Avg('ratings__score'),
            rating_count=Count('ratings')
        ).filter(
            avg_rating__gte=min_rating,
            rating_count__gte=min_rating_count
        ).order_by('-avg_rating')[:limit]
        
        return highly_rated
