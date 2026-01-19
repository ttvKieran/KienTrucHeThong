from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from store.models import Order, Shipping
from store.serializers import (
    OrderSerializer, 
    CreateOrderSerializer, 
    ShippingSerializer
)
from store.services.order_service import OrderService


class OrderViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing orders
    """
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer
    
    def get_queryset(self):
        """
        Return orders for the current customer
        Staff can see all orders
        """
        user = self.request.user
        if user.is_staff:
            return Order.objects.all()
        
        try:
            customer = user.customer
            return Order.objects.filter(customer=customer)
        except:
            return Order.objects.none()
    
    def create(self, request):
        """
        Create a new order from cart
        """
        serializer = CreateOrderSerializer(data=request.data)
        if serializer.is_valid():
            try:
                # Get customer
                customer = request.user.customer
                
                # Get or create active cart
                from store.models import Cart
                cart = Cart.objects.filter(customer=customer, is_active=True).first()
                
                if not cart:
                    return Response(
                        {'error': 'No active cart found'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
                # Create order
                order = OrderService.create_order_from_cart(
                    customer=customer,
                    cart=cart,
                    shipping_id=serializer.validated_data['shipping_id'],
                    payment_method=serializer.validated_data['payment_method'],
                    shipping_address=serializer.validated_data['shipping_address'],
                    note=serializer.validated_data.get('note', '')
                )
                
                response_serializer = OrderSerializer(order)
                return Response(response_serializer.data, status=status.HTTP_201_CREATED)
            
            except ValueError as e:
                return Response(
                    {'error': str(e)},
                    status=status.HTTP_400_BAD_REQUEST
                )
            except Exception as e:
                return Response(
                    {'error': 'Failed to create order: ' + str(e)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """
        Cancel an order
        """
        try:
            customer = request.user.customer if not request.user.is_staff else None
            order = OrderService.cancel_order(pk, customer)
            
            if order:
                serializer = OrderSerializer(order)
                return Response(serializer.data)
            else:
                return Response(
                    {'error': 'Order not found or cannot be cancelled'},
                    status=status.HTTP_404_NOT_FOUND
                )
        except ValueError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def update_status(self, request, pk=None):
        """
        Update order status (staff only)
        """
        if not request.user.is_staff:
            return Response(
                {'error': 'Permission denied'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        new_status = request.data.get('status')
        if not new_status:
            return Response(
                {'error': 'Status is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        order = OrderService.update_order_status(pk, new_status)
        
        if order:
            serializer = OrderSerializer(order)
            return Response(serializer.data)
        else:
            return Response(
                {'error': 'Order not found'},
                status=status.HTTP_404_NOT_FOUND
            )


class ShippingViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing available shipping methods
    """
    queryset = Shipping.objects.filter(is_active=True)
    serializer_class = ShippingSerializer
    permission_classes = [IsAuthenticated]


# Function-based views for simpler URL routing
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def order_list_create(request):
    """
    GET: List all orders for current user
    POST: Create new order from cart
    """
    if request.method == 'GET':
        # Get orders for current user
        user = request.user
        if user.is_staff:
            orders = Order.objects.all()
        else:
            try:
                customer = user.customer
                orders = Order.objects.filter(customer=customer)
            except:
                orders = Order.objects.none()
        
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        # Create order
        serializer = CreateOrderSerializer(data=request.data)
        if serializer.is_valid():
            try:
                # Get customer
                try:
                    customer = request.user.customer
                except:
                    return Response(
                        {'error': 'Customer profile not found. Please complete your profile first.'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
                # Get or create active cart
                from store.models import Cart
                cart = Cart.objects.filter(customer=customer, is_active=True).first()
                
                if not cart:
                    return Response(
                        {'error': 'No active cart found'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
                # Create order
                order = OrderService.create_order_from_cart(
                    customer=customer,
                    cart=cart,
                    shipping_id=serializer.validated_data['shipping_id'],
                    payment_method=serializer.validated_data['payment_method'],
                    shipping_address=serializer.validated_data['shipping_address'],
                    note=serializer.validated_data.get('note', '')
                )
                
                response_serializer = OrderSerializer(order)
                return Response(response_serializer.data, status=status.HTTP_201_CREATED)
            
            except ValueError as e:
                return Response(
                    {'error': str(e)},
                    status=status.HTTP_400_BAD_REQUEST
                )
            except Exception as e:
                return Response(
                    {'error': 'Failed to create order: ' + str(e)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def order_detail(request, order_id):
    """
    Get order detail
    """
    user = request.user
    if user.is_staff:
        order = Order.objects.filter(id=order_id).first()
    else:
        try:
            customer = user.customer
            order = Order.objects.filter(id=order_id, customer=customer).first()
        except:
            order = None
    
    if not order:
        return Response(
            {'error': 'Order not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    serializer = OrderSerializer(order)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def cancel_order(request, order_id):
    """
    Cancel an order
    """
    try:
        customer = request.user.customer if not request.user.is_staff else None
        order = OrderService.cancel_order(order_id, customer)
        
        if order:
            serializer = OrderSerializer(order)
            return Response(serializer.data)
        else:
            return Response(
                {'error': 'Order not found or cannot be cancelled'},
                status=status.HTTP_404_NOT_FOUND
            )
    except ValueError as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_order_status(request, order_id):
    """
    Update order status (staff only)
    """
    if not request.user.is_staff:
        return Response(
            {'error': 'Permission denied'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    new_status = request.data.get('status')
    if not new_status:
        return Response(
            {'error': 'Status is required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    order = OrderService.update_order_status(order_id, new_status)
    
    if order:
        serializer = OrderSerializer(order)
        return Response(serializer.data)
    else:
        return Response(
            {'error': 'Order not found'},
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def shipping_list(request):
    """
    Get list of active shipping methods
    """
    shipping_methods = Shipping.objects.filter(is_active=True)
    serializer = ShippingSerializer(shipping_methods, many=True)
    return Response(serializer.data)
