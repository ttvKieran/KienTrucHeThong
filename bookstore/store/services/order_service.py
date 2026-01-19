from django.db import transaction
from django.db.models import Avg
from store.models import Order, OrderItem, Book, Shipping, Payment, Cart


class OrderService:
    """
    Service class for handling order-related business logic
    """
    
    @staticmethod
    @transaction.atomic
    def create_order_from_cart(customer, cart, shipping_id, payment_method, shipping_address, note=''):
        """
        Create an order from a customer's cart
        
        Args:
            customer: Customer instance
            cart: Cart instance
            shipping_id: ID of the shipping method
            payment_method: Name of the payment method
            shipping_address: Delivery address
            note: Optional note
            
        Returns:
            Order instance
            
        Raises:
            ValueError: If cart is empty or items are out of stock
        """
        # Get cart items
        cart_items = cart.cartitem_set.all()
        
        if not cart_items.exists():
            raise ValueError("Cart is empty")
        
        # Validate stock and calculate total
        total_price = 0
        order_items_data = []
        
        for cart_item in cart_items:
            book = cart_item.book
            if book.stock < cart_item.quantity:
                raise ValueError(f"Insufficient stock for {book.title}")
            
            subtotal = cart_item.quantity * cart_item.price
            total_price += subtotal
            
            order_items_data.append({
                'book': book,
                'quantity': cart_item.quantity,
                'price': cart_item.price,
                'subtotal': subtotal
            })
        
        # Get shipping method and add fee
        shipping = Shipping.objects.get(id=shipping_id, is_active=True)
        total_price += shipping.fee
        
        # Create payment record
        payment = Payment.objects.create(
            method_name=payment_method,
            status='pending'
        )
        
        # Create order
        order = Order.objects.create(
            customer=customer,
            total_price=total_price,
            shipping=shipping,
            payment=payment,
            shipping_address=shipping_address,
            note=note,
            status='pending'
        )
        
        # Create order items and update stock
        for item_data in order_items_data:
            OrderItem.objects.create(
                order=order,
                **item_data
            )
            
            # Reduce stock
            book = item_data['book']
            book.stock -= item_data['quantity']
            book.save()
        
        # Mark cart as inactive
        cart.is_active = False
        cart.save()
        
        return order
    
    @staticmethod
    def get_order_by_id(order_id, customer=None):
        """
        Get order by ID, optionally filtered by customer
        """
        if customer:
            return Order.objects.filter(id=order_id, customer=customer).first()
        return Order.objects.filter(id=order_id).first()
    
    @staticmethod
    def get_customer_orders(customer):
        """
        Get all orders for a customer
        """
        return Order.objects.filter(customer=customer).order_by('-created_at')
    
    @staticmethod
    def update_order_status(order_id, status):
        """
        Update order status
        """
        try:
            order = Order.objects.get(id=order_id)
            order.status = status
            order.save()
            return order
        except Order.DoesNotExist:
            return None
    
    @staticmethod
    def cancel_order(order_id, customer=None):
        """
        Cancel an order and restore stock
        """
        try:
            if customer:
                order = Order.objects.get(id=order_id, customer=customer)
            else:
                order = Order.objects.get(id=order_id)
            
            if order.status not in ['pending', 'confirmed']:
                raise ValueError("Cannot cancel order in current status")
            
            # Restore stock
            for order_item in order.items.all():
                book = order_item.book
                book.stock += order_item.quantity
                book.save()
            
            # Update order status
            order.status = 'cancelled'
            order.save()
            
            # Update payment status
            if order.payment:
                order.payment.status = 'refunded'
                order.payment.save()
            
            return order
        except Order.DoesNotExist:
            return None
