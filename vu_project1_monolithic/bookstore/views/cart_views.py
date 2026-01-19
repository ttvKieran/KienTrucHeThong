from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ..serializers import CartSerializer, CartItemSerializer, AddToCartSerializer
from ..services.cart_service import CartService


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_cart(request):
    """
    API endpoint to add books to shopping cart
    POST /api/cart/add
    """
    serializer = AddToCartSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    book_id = serializer.validated_data['book_id']
    quantity = serializer.validated_data['quantity']
    
    # Use service layer for business logic
    cart_item, created, error = CartService.add_item_to_cart(
        request.user, book_id, quantity
    )
    
    if error:
        return Response({
            'error': error
        }, status=status.HTTP_400_BAD_REQUEST)
    
    return Response({
        'message': 'Book added to cart successfully',
        'cart_item': CartItemSerializer(cart_item).data
    }, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_cart(request):
    """
    API endpoint to view shopping cart contents
    GET /api/cart
    """
    try:
        # Use service layer to get cart
        cart = CartService.get_cart_contents(request.user)
        
        if cart:
            serializer = CartSerializer(cart)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({
                'message': 'Cart is empty',
                'items': [],
                'total_items': 0,
                'total_price': 0
            }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({
            'error': str(e)
        }, status=status.HTTP_404_NOT_FOUND)


@api_view(['PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def manage_cart_item(request, item_id):
    """
    API endpoint to update or remove cart item
    PUT /api/cart/item/<item_id> - Update quantity
    DELETE /api/cart/item/<item_id> - Remove item
    """
    if request.method == 'DELETE':
        # Use service layer to remove item
        success, error = CartService.remove_cart_item(request.user, item_id)
        
        if success:
            return Response({
                'message': 'Item removed from cart successfully'
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'error': error
            }, status=status.HTTP_404_NOT_FOUND)
    
    elif request.method == 'PUT':
        quantity = request.data.get('quantity')
        if not quantity or int(quantity) < 1:
            return Response({
                'error': 'Quantity must be at least 1'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Use service layer to update quantity
        cart_item, error = CartService.update_cart_item_quantity(
            request.user, item_id, int(quantity)
        )
        
        if error:
            return Response({
                'error': error
            }, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({
            'message': 'Cart item updated successfully',
            'cart_item': CartItemSerializer(cart_item).data
        }, status=status.HTTP_200_OK)
