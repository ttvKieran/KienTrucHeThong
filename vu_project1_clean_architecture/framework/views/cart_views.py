"""
Cart Views
Framework layer - controllers that handle HTTP requests
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from domain.exceptions import (
    BookNotFoundException, 
    CustomerNotFoundException, 
    InsufficientStockException
)
from usecases.cart import (
    AddItemToCartUseCase,
    ViewCartUseCase,
    UpdateCartItemUseCase,
    RemoveItemFromCartUseCase
)
from framework.dependencies import inject_dependencies


@inject_dependencies
class CartView(APIView):
    """
    Controller for viewing cart
    """
    permission_classes = [IsAuthenticated]
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.view_cart_use_case = None  # Will be injected
    
    def get(self, request):
        """GET /api/cart/"""
        try:
            user_id = request.user.id
            
            # Execute use case
            cart = self.view_cart_use_case.execute(user_id)
            
            # Convert entity to response format
            from framework.serializers import CartSerializer
            serializer = CartSerializer(cart)
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except CustomerNotFoundException as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


@inject_dependencies
class AddToCartView(APIView):
    """
    Controller for adding item to cart
    """
    permission_classes = [IsAuthenticated]
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_item_use_case = None  # Will be injected
    
    def post(self, request):
        """
        POST /api/cart/add/
        Body: {book_id: int, quantity: int}
        """
        try:
            user_id = request.user.id
            book_id = request.data.get('book_id')
            quantity = request.data.get('quantity', 1)
            
            # Validate input
            if not book_id:
                return Response(
                    {'error': 'book_id is required'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Execute use case
            cart = self.add_item_use_case.execute(user_id, book_id, quantity)
            
            # Convert entity to response format
            from framework.serializers import CartSerializer
            serializer = CartSerializer(cart)
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        except (BookNotFoundException, CustomerNotFoundException) as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_404_NOT_FOUND
            )
        except InsufficientStockException as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

@inject_dependencies

class UpdateCartItemView(APIView):
    """
    Controller for updating cart item
    """
    permission_classes = [IsAuthenticated]
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.update_item_use_case = None  # Will be injected
    
    def put(self, request, book_id):
        """
        PUT /api/cart/update/<book_id>/
        Body: {quantity: int}
        """
        try:
            user_id = request.user.id
            quantity = request.data.get('quantity')
            
            # Validate input
            if quantity is None:
                return Response(
                    {'error': 'quantity is required'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Execute use case
            cart = self.update_item_use_case.execute(user_id, book_id, quantity)
            
            # Convert entity to response format
            from framework.serializers import CartSerializer
            serializer = CartSerializer(cart)
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except (BookNotFoundException, CustomerNotFoundException) as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_404_NOT_FOUND
            )
        except InsufficientStockException as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

@inject_dependencies

class RemoveFromCartView(APIView):
    """
    Controller for removing item from cart
    """
    permission_classes = [IsAuthenticated]
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.remove_item_use_case = None  # Will be injected
    
    def delete(self, request, book_id):
        """DELETE /api/cart/remove/<book_id>/"""
        try:
            user_id = request.user.id
            
            # Execute use case
            cart = self.remove_item_use_case.execute(user_id, book_id)
            
            # Convert entity to response format
            from framework.serializers import CartSerializer
            serializer = CartSerializer(cart)
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except (BookNotFoundException, CustomerNotFoundException) as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
