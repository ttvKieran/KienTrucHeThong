"""
Cart Repository Implementation
Infrastructure layer - implements repository interface using Django ORM
"""
from typing import Optional
from decimal import Decimal
from domain.entities import Cart, CartItem
from interfaces.repositories import ICartRepository
from infrastructure.models import CartModel, CartItemModel, BookModel


class DjangoCartRepository(ICartRepository):
    """
    Django ORM implementation of Cart repository
    """
    
    def _cart_item_to_entity(self, model: CartItemModel) -> CartItem:
        """Convert Django cart item model to domain entity"""
        return CartItem(
            id=model.id,
            book_id=model.book.id,
            book_title=model.book.title,
            quantity=model.quantity,
            price=Decimal(str(model.price))
        )
    
    def _to_entity(self, model: CartModel) -> Cart:
        """Convert Django model to domain entity"""
        items = [
            self._cart_item_to_entity(item_model)
            for item_model in model.items.all()
        ]
        
        return Cart(
            id=model.id,
            customer_id=model.customer.id,
            items=items,
            created_at=model.created_at
        )
    
    def get_by_customer_id(self, customer_id: int) -> Optional[Cart]:
        """Get cart by customer ID"""
        try:
            model = CartModel.objects.prefetch_related('items__book').get(
                customer__id=customer_id
            )
            return self._to_entity(model)
        except CartModel.DoesNotExist:
            return None
    
    def get_by_id(self, cart_id: int) -> Optional[Cart]:
        """Get cart by ID"""
        try:
            model = CartModel.objects.prefetch_related('items__book').get(id=cart_id)
            return self._to_entity(model)
        except CartModel.DoesNotExist:
            return None
    
    def save(self, cart: Cart) -> Cart:
        """Save or update cart"""
        from infrastructure.models import CustomerModel
        
        if cart.id:
            # Update existing cart
            try:
                cart_model = CartModel.objects.get(id=cart.id)
            except CartModel.DoesNotExist:
                # Create new if doesn't exist
                customer = CustomerModel.objects.get(id=cart.customer_id)
                cart_model = CartModel.objects.create(customer=customer)
        else:
            # Create new cart
            customer = CustomerModel.objects.get(id=cart.customer_id)
            cart_model = CartModel.objects.create(customer=customer)
        
        # Sync cart items
        # Get existing items
        existing_items = {item.book.id: item for item in cart_model.items.all()}
        
        # Update or create items
        for item in cart.items:
            if item.book_id in existing_items:
                # Update existing item
                item_model = existing_items[item.book_id]
                item_model.quantity = item.quantity
                item_model.price = item.price
                item_model.save()
                del existing_items[item.book_id]
            else:
                # Create new item
                book = BookModel.objects.get(id=item.book_id)
                CartItemModel.objects.create(
                    cart=cart_model,
                    book=book,
                    quantity=item.quantity,
                    price=item.price
                )
        
        # Delete items not in cart anymore
        for book_id, item_model in existing_items.items():
            item_model.delete()
        
        # Reload and return
        cart_model.refresh_from_db()
        return self._to_entity(cart_model)
    
    def save_item(self, cart_id: int, item: CartItem) -> CartItem:
        """Save or update cart item"""
        cart_model = CartModel.objects.get(id=cart_id)
        book = BookModel.objects.get(id=item.book_id)
        
        item_model, created = CartItemModel.objects.update_or_create(
            cart=cart_model,
            book=book,
            defaults={
                'quantity': item.quantity,
                'price': item.price
            }
        )
        
        return self._cart_item_to_entity(item_model)
    
    def delete_item(self, cart_id: int, book_id: int) -> bool:
        """Delete cart item"""
        try:
            item = CartItemModel.objects.get(cart__id=cart_id, book__id=book_id)
            item.delete()
            return True
        except CartItemModel.DoesNotExist:
            return False
    
    def clear(self, cart_id: int) -> bool:
        """Clear all items from cart"""
        try:
            cart = CartModel.objects.get(id=cart_id)
            cart.items.all().delete()
            return True
        except CartModel.DoesNotExist:
            return False
