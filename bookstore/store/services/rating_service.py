from store.models import Rating


class RatingService:
    """
    Service class for handling rating-related business logic
    """
    
    @staticmethod
    def create_or_update_rating(customer, book, score, review=''):
        """
        Create or update a rating for a book
        
        Args:
            customer: Customer instance
            book: Book instance
            score: Rating score (1-5)
            review: Optional review text
            
        Returns:
            Rating instance
        """
        rating, created = Rating.objects.update_or_create(
            customer=customer,
            book=book,
            defaults={
                'score': score,
                'review': review
            }
        )
        return rating
    
    @staticmethod
    def get_book_ratings(book):
        """
        Get all ratings for a book
        """
        return Rating.objects.filter(book=book).order_by('-created_at')
    
    @staticmethod
    def get_customer_ratings(customer):
        """
        Get all ratings by a customer
        """
        return Rating.objects.filter(customer=customer).order_by('-created_at')
    
    @staticmethod
    def delete_rating(rating_id, customer=None):
        """
        Delete a rating
        """
        try:
            if customer:
                rating = Rating.objects.get(id=rating_id, customer=customer)
            else:
                rating = Rating.objects.get(id=rating_id)
            rating.delete()
            return True
        except Rating.DoesNotExist:
            return False
