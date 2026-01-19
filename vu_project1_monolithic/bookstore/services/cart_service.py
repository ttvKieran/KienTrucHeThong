"""
Cart Service - Business Logic Layer
Handles shopping cart operations
"""
from django.db import transaction
from ..models import Customer, Book, Cart, CartItem


class CartService:
    """Service class for shopping cart operations"""
    
    @staticmethod
    def get_customer_cart(user):
        """
        Get or create cart for customer
        
        Args:
            user: User object
            
        Returns:
            Cart object or None if customer not found
            
        Raises:
            Customer.DoesNotExist: If customer profile not found
        """
        customer = Customer.objects.get(user=user)
        cart, created = Cart.objects.get_or_create(customer=customer)
        return cart
    
    @staticmethod
    def add_item_to_cart(user, book_id, quantity):
        """
        Add item to shopping cart
        
        Args:
            user: User object
            book_id: Book ID to add
            quantity: Quantity to add
            
        Returns:
            tuple: (cart_item, created: bool, error_message: str or None)
        """
        try:
            # Get customer
            customer = Customer.objects.get(user=user)
            
            # Get book
            book = Book.objects.get(id=book_id)
            
            # Business rule: Check stock availability
            if book.stock < quantity:
                return None, False, f'Not enough stock. Only {book.stock} items available'
            
            with transaction.atomic():
                # Get or create cart
                cart, created = Cart.objects.get_or_create(customer=customer)
                
                # Check if book already in cart
                cart_item, item_created = CartItem.objects.get_or_create(
                    cart=cart,
                    book=book,
                    defaults={'quantity': quantity, 'price': book.stock}  # Using stock as price
                )
                
                if not item_created:
                    # Business rule: Update quantity if item exists
                    new_quantity = cart_item.quantity + quantity
                    if book.stock < new_quantity:
                        return None, False, f'Not enough stock. Only {book.stock} items available. You already have {cart_item.quantity} in cart'
                    
                    cart_item.quantity = new_quantity
                    cart_item.save()
                
                return cart_item, item_created, None
                
        except Customer.DoesNotExist:
            return None, False, 'Customer profile not found'
        except Book.DoesNotExist:
            return None, False, 'Book not found'
        except Exception as e:
            return None, False, str(e)
    
    @staticmethod
    def get_cart_contents(user):
        """
        Get cart contents for user
        
        Args:
            user: User object
            
        Returns:
            Cart object or None
            
        Raises:
            Customer.DoesNotExist: If customer not found
        """
        customer = Customer.objects.get(user=user)
        try:
            return Cart.objects.get(customer=customer)
        except Cart.DoesNotExist:
            return None
    
    @staticmethod
    def update_cart_item_quantity(user, item_id, new_quantity):
        """
        Update quantity of item in cart
        
        Args:
            user: User object
            item_id: CartItem ID
            new_quantity: New quantity
            
        Returns:
            tuple: (cart_item, error_message: str or None)
        """
        try:
            customer = Customer.objects.get(user=user)
            cart = Cart.objects.get(customer=customer)
            cart_item = CartItem.objects.get(id=item_id, cart=cart)
            
            # Business rule: Quantity must be at least 1
            if new_quantity < 1:
                return None, 'Quantity must be at least 1'
            
            # Business rule: Check stock availability
            if cart_item.book.stock < new_quantity:
                return None, f'Not enough stock. Only {cart_item.book.stock} items available'
            
            cart_item.quantity = new_quantity
            cart_item.save()
            
            return cart_item, None
            
        except Customer.DoesNotExist:
            return None, 'Customer profile not found'
        except Cart.DoesNotExist:
            return None, 'Cart not found'
        except CartItem.DoesNotExist:
            return None, 'Cart item not found'
        except Exception as e:
            return None, str(e)
    
    @staticmethod
    def remove_cart_item(user, item_id):
        """
        Remove item from cart
        
        Args:
            user: User object
            item_id: CartItem ID
            
        Returns:
            tuple: (success: bool, error_message: str or None)
        """
        try:
            customer = Customer.objects.get(user=user)
            cart = Cart.objects.get(customer=customer)
            cart_item = CartItem.objects.get(id=item_id, cart=cart)
            
            cart_item.delete()
            return True, None
            
        except Customer.DoesNotExist:
            return False, 'Customer profile not found'
        except Cart.DoesNotExist:
            return False, 'Cart not found'
        except CartItem.DoesNotExist:
            return False, 'Cart item not found'
        except Exception as e:
            return False, str(e)
    
    @staticmethod
    def calculate_cart_total(cart):
        """
        Calculate total price and items in cart
        
        Args:
            cart: Cart object
            
        Returns:
            tuple: (total_items: int, total_price: Decimal)
        """
        items = cart.cartitem_set.all()
        total_items = items.count()
        total_price = sum(item.quantity * item.price for item in items)
        return total_items, total_price
