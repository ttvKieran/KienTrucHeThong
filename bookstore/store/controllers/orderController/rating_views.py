from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from store.models import Rating, Book
from store.serializers import RatingSerializer, CreateRatingSerializer
from store.services.rating_service import RatingService


class RatingViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing book ratings
    """
    permission_classes = [IsAuthenticated]
    serializer_class = RatingSerializer
    
    def get_queryset(self):
        """
        Return ratings based on filters
        """
        queryset = Rating.objects.all()
        
        # Filter by book
        book_id = self.request.query_params.get('book_id')
        if book_id:
            queryset = queryset.filter(book_id=book_id)
        
        # Filter by customer (show only their ratings)
        if not self.request.user.is_staff:
            try:
                customer = self.request.user.customer
                queryset = queryset.filter(customer=customer)
            except:
                queryset = Rating.objects.none()
        
        return queryset
    
    def create(self, request):
        """
        Create or update a rating
        """
        serializer = CreateRatingSerializer(data=request.data)
        if serializer.is_valid():
            try:
                customer = request.user.customer
                book_id = serializer.validated_data['book']
                book = Book.objects.get(id=book_id.id)
                
                rating = RatingService.create_or_update_rating(
                    customer=customer,
                    book=book,
                    score=serializer.validated_data['score'],
                    review=serializer.validated_data.get('review', '')
                )
                
                response_serializer = RatingSerializer(rating)
                return Response(response_serializer.data, status=status.HTTP_201_CREATED)
            
            except Exception as e:
                return Response(
                    {'error': str(e)},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, pk=None):
        """
        Delete a rating
        """
        customer = request.user.customer if not request.user.is_staff else None
        success = RatingService.delete_rating(pk, customer)
        
        if success:
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(
                {'error': 'Rating not found'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=False, methods=['get'])
    def my_ratings(self, request):
        """
        Get all ratings by the current customer
        """
        try:
            customer = request.user.customer
            ratings = RatingService.get_customer_ratings(customer)
            serializer = RatingSerializer(ratings, many=True)
            return Response(serializer.data)
        except:
            return Response(
                {'error': 'Customer profile not found'},
                status=status.HTTP_404_NOT_FOUND
            )
