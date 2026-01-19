"""
Cart Service Views
"""
from datetime import datetime
from decimal import Decimal
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from django.db import transaction

from .models import Cart, CartItem, Order, OrderItem
from .serializers import (
    CartSerializer,
    AddToCartSerializer,
    UpdateCartItemSerializer,
    OrderSerializer
)
from .service_clients import BookServiceClient, UserServiceClient


@api_view(['GET'])
def health_check(request):
    """Health check endpoint"""
    return Response({
        'status': 'healthy',
        'service': 'cart-service',
        'timestamp': datetime.now().isoformat()
    })


def get_user_id_from_request(request):
    """Extract user_id from request params (set by API Gateway)"""
    user_id = request.query_params.get('user_id') or request.data.get('user_id')
    if user_id:
        try:
            return int(user_id)
        except ValueError:
            return None
    return None


class CartView(APIView):
    """
    View and manage shopping cart
    GET /api/cart/ - View cart
    """
    
    def get(self, request):
        """Get user's cart"""
        user_id = get_user_id_from_request(request)
        
        if not user_id:
            return Response(
                {'error': 'User ID required'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        # Get or create cart for user
        cart, created = Cart.objects.get_or_create(user_id=user_id)
        
        serializer = CartSerializer(cart)
        return Response(serializer.data)


class AddToCartView(APIView):
    """
    Add item to cart
    POST /api/cart/add/
    Body: {book_id, quantity}
    """
    
    def post(self, request):
        """Add item to cart"""
        user_id = get_user_id_from_request(request)
        
        if not user_id:
            return Response(
                {'error': 'User ID required'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        serializer = AddToCartSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        
        book_id = serializer.validated_data['book_id']
        quantity = serializer.validated_data['quantity']
        
        # Check book stock via Book Service
        stock_info = BookServiceClient.check_stock(book_id, quantity)
        
        if not stock_info:
            return Response(
                {'error': 'Unable to verify book availability'},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
        
        if not stock_info.get('available'):
            return Response(
                {'error': f"Insufficient stock. Available: {stock_info.get('current_stock', 0)}"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get or create cart
        cart, created = Cart.objects.get_or_create(user_id=user_id)
        
        # Add or update cart item
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            book_id=book_id,
            defaults={
                'book_title': stock_info['title'],
                'quantity': quantity,
                'price': Decimal(stock_info['price'])
            }
        )
        
        if not created:
            # Update existing item
            cart_item.quantity += quantity
            cart_item.save()
        
        return Response({
            'message': 'Item added to cart',
            'cart': CartSerializer(cart).data
        }, status=status.HTTP_201_CREATED)


class UpdateCartView(APIView):
    """
    Update cart item quantity
    PUT /api/cart/update/
    Body: {book_id, quantity}
    """
    
    def put(self, request):
        """Update cart item quantity"""
        user_id = get_user_id_from_request(request)
        
        if not user_id:
            return Response(
                {'error': 'User ID required'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        serializer = UpdateCartItemSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        
        book_id = serializer.validated_data['book_id']
        quantity = serializer.validated_data['quantity']
        
        # Get cart
        try:
            cart = Cart.objects.get(user_id=user_id)
        except Cart.DoesNotExist:
            return Response(
                {'error': 'Cart not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Get cart item
        try:
            cart_item = CartItem.objects.get(cart=cart, book_id=book_id)
        except CartItem.DoesNotExist:
            return Response(
                {'error': 'Item not found in cart'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Check stock
        stock_info = BookServiceClient.check_stock(book_id, quantity)
        
        if not stock_info or not stock_info.get('available'):
            return Response(
                {'error': 'Insufficient stock'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Update quantity
        cart_item.quantity = quantity
        cart_item.save()
        
        return Response({
            'message': 'Cart updated',
            'cart': CartSerializer(cart).data
        })


class RemoveFromCartView(APIView):
    """
    Remove item from cart
    DELETE /api/cart/remove/{book_id}/
    """
    
    def delete(self, request, book_id):
        """Remove item from cart"""
        user_id = get_user_id_from_request(request)
        
        if not user_id:
            return Response(
                {'error': 'User ID required'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        try:
            cart = Cart.objects.get(user_id=user_id)
            cart_item = CartItem.objects.get(cart=cart, book_id=book_id)
            cart_item.delete()
            
            return Response({
                'message': 'Item removed from cart',
                'cart': CartSerializer(cart).data
            })
            
        except (Cart.DoesNotExist, CartItem.DoesNotExist):
            return Response(
                {'error': 'Item not found'},
                status=status.HTTP_404_NOT_FOUND
            )


class CheckoutView(APIView):
    """
    Checkout - Create order from cart
    POST /api/cart/checkout/
    """
    
    def post(self, request):
        """Checkout cart and create order"""
        user_id = get_user_id_from_request(request)
        
        if not user_id:
            return Response(
                {'error': 'User ID required'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        try:
            cart = Cart.objects.get(user_id=user_id)
        except Cart.DoesNotExist:
            return Response(
                {'error': 'Cart not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        if not cart.items.exists():
            return Response(
                {'error': 'Cart is empty'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Verify stock for all items and reduce stock
        with transaction.atomic():
            # Create order
            order = Order.objects.create(
                user_id=user_id,
                total=cart.get_total(),
                status='pending'
            )
            
            # Create order items and reduce stock
            for cart_item in cart.items.all():
                # Verify stock one more time
                stock_info = BookServiceClient.check_stock(
                    cart_item.book_id,
                    cart_item.quantity
                )
                
                if not stock_info or not stock_info.get('available'):
                    # Rollback will happen automatically
                    return Response(
                        {'error': f'Book "{cart_item.book_title}" is out of stock'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
                # Create order item
                OrderItem.objects.create(
                    order=order,
                    book_id=cart_item.book_id,
                    book_title=cart_item.book_title,
                    quantity=cart_item.quantity,
                    price=cart_item.price,
                    subtotal=cart_item.get_subtotal()
                )
                
                # Reduce stock
                success = BookServiceClient.update_stock(
                    cart_item.book_id,
                    cart_item.quantity,
                    operation='decrease'
                )
                
                if not success:
                    return Response(
                        {'error': 'Failed to update stock'},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR
                    )
            
            # Clear cart
            cart.items.all().delete()
            
            return Response({
                'message': 'Order created successfully',
                'order': OrderSerializer(order).data
            }, status=status.HTTP_201_CREATED)


class OrderListView(APIView):
    """
    List user's orders
    GET /api/orders/
    """
    
    def get(self, request):
        """Get user's order history"""
        user_id = get_user_id_from_request(request)
        
        if not user_id:
            return Response(
                {'error': 'User ID required'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        orders = Order.objects.filter(user_id=user_id)
        serializer = OrderSerializer(orders, many=True)
        
        return Response({
            'count': orders.count(),
            'orders': serializer.data
        })
