from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q, Avg, Count
from store.models.book import Book, Category, Rating
from store.models.customer import Customer, Address
from store.models.order import Order, OrderItem, Shipping, Payment, Cart, CartItem
from store.models.staff import Staff
from decimal import Decimal

# ================ AUTHENTICATION VIEWS ================

def login_view(request):
    """Đăng nhập"""
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_type = request.POST.get('user_type', 'customer')
        
        if user_type == 'customer':
            try:
                user = Customer.objects.get(email=email, password=password)
                request.session['user_id'] = user.id
                request.session['user_type'] = 'customer'
                request.session['user_name'] = user.name
                messages.success(request, f'Chào mừng {user.name}!')
                return redirect('web_home')
            except Customer.DoesNotExist:
                messages.error(request, 'Email hoặc mật khẩu không đúng!')
        else:
            try:
                user = Staff.objects.get(email=email, password=password)
                request.session['user_id'] = user.id
                request.session['user_type'] = 'staff'
                request.session['user_name'] = user.name
                messages.success(request, f'Chào mừng {user.name}!')
                return redirect('web_staff_dashboard')
            except Staff.DoesNotExist:
                messages.error(request, 'Thông tin đăng nhập không đúng!')
    
    return render(request, 'auth/login.html')


def register_view(request):
    """Đăng ký tài khoản khách hàng"""
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        # Validate
        if password != confirm_password:
            messages.error(request, 'Mật khẩu xác nhận không khớp!')
            return render(request, 'auth/register.html')
        
        if Customer.objects.filter(email=email).exists():
            messages.error(request, 'Email đã được sử dụng!')
            return render(request, 'auth/register.html')
        
        # Create address
        address = Address.objects.create(
            house_number=request.POST.get('house_number'),
            street=request.POST.get('street'),
            province=request.POST.get('province'),
            building=''
        )
        
        # Create customer
        customer = Customer.objects.create(
            name=name,
            email=email,
            password=password,
            address=address
        )
        
        messages.success(request, 'Đăng ký thành công! Vui lòng đăng nhập.')
        return redirect('web_login')
    
    return render(request, 'auth/register.html')


def logout_view(request):
    """Đăng xuất"""
    request.session.flush()
    messages.success(request, 'Đã đăng xuất!')
    return redirect('web_login')


# ================ HELPER FUNCTIONS ================

def get_current_user(request):
    """Get current logged in user"""
    user_id = request.session.get('user_id')
    user_type = request.session.get('user_type')
    
    if not user_id:
        return None, None
    
    if user_type == 'customer':
        try:
            return Customer.objects.get(id=user_id), 'customer'
        except Customer.DoesNotExist:
            return None, None
    elif user_type == 'staff':
        try:
            return Staff.objects.get(id=user_id), 'staff'
        except Staff.DoesNotExist:
            return None, None
    
    return None, None


def require_login(view_func):
    """Decorator to require login"""
    def wrapper(request, *args, **kwargs):
        user, user_type = get_current_user(request)
        if not user:
            messages.warning(request, 'Vui lòng đăng nhập!')
            return redirect('web_login')
        return view_func(request, *args, **kwargs)
    return wrapper


def require_staff(view_func):
    """Decorator to require staff login"""
    def wrapper(request, *args, **kwargs):
        user, user_type = get_current_user(request)
        if not user or user_type != 'staff':
            messages.error(request, 'Bạn không có quyền truy cập!')
            return redirect('web_login')
        return view_func(request, *args, **kwargs)
    return wrapper


# ================ BOOK VIEWS ================

def book_list(request):
    """Trang chủ - danh sách sách với tìm kiếm"""
    books = Book.objects.all()
    categories = Category.objects.all()
    
    # Search
    search_query = request.GET.get('q', '')
    if search_query:
        books = books.filter(
            Q(title__icontains=search_query) |
            Q(author__icontains=search_query)
        )
    
    # Filter by category
    selected_category = request.GET.get('category', '')
    if selected_category:
        books = books.filter(category_id=selected_category)
    
    context = {
        'books': books,
        'categories': categories,
        'search_query': search_query,
        'selected_category': selected_category,
    }
    return render(request, 'book/list.html', context)


def book_detail(request, book_id):
    """Chi tiết sách"""
    book = get_object_or_404(Book, id=book_id)
    
    # Get ratings
    ratings = Rating.objects.filter(book=book).select_related('customer')
    avg_rating = ratings.aggregate(Avg('score'))['score__avg']
    
    # Similar books (same category)
    similar_books = Book.objects.filter(
        category=book.category
    ).exclude(id=book.id)[:4]
    
    context = {
        'book': book,
        'ratings': ratings,
        'avg_rating': avg_rating,
        'similar_books': similar_books,
    }
    return render(request, 'book/detail.html', context)


# ================ CART VIEWS ================

@require_login
def cart_view(request):
    """Xem giỏ hàng"""
    user, user_type = get_current_user(request)
    if user_type != 'customer':
        messages.error(request, 'Chỉ khách hàng mới có giỏ hàng!')
        return redirect('web_home')
    
    customer = user
    
    cart, _ = Cart.objects.get_or_create(customer=customer)
    cart_items = CartItem.objects.filter(cart=cart).select_related('book')
    
    total = sum(item.book.price * item.quantity for item in cart_items)
    
    context = {
        'cart_items': cart_items,
        'total': total,
    }
    return render(request, 'cart/view.html', context)


@require_login
def add_to_cart(request, book_id):
    """Thêm sách vào giỏ"""
    if request.method == 'POST':
        user, user_type = get_current_user(request)
        if user_type != 'customer':
            messages.error(request, 'Chỉ khách hàng mới có thể thêm vào giỏ!')
            return redirect('web_book_detail', book_id=book_id)
        
        customer = user
        book = get_object_or_404(Book, id=book_id)
        
        quantity = int(request.POST.get('quantity', 1))
        
        # Check stock
        if book.stock_quantity < quantity:
            messages.error(request, f'Không đủ hàng trong kho. Chỉ còn {book.stock_quantity} cuốn.')
            return redirect('web_book_detail', book_id=book_id)
        
        # Get or create cart
        cart, _ = Cart.objects.get_or_create(customer=customer)
        
        # Add to cart
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            book=book,
            defaults={'quantity': quantity}
        )
        
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
        
        messages.success(request, f'Đã thêm "{book.title}" vào giỏ hàng!')
        return redirect('web_cart')
    
    return redirect('web_home')


@require_login
def update_cart_item(request, item_id):
    """Cập nhật số lượng trong giỏ"""
    if request.method == 'POST':
        cart_item = get_object_or_404(CartItem, id=item_id)
        quantity = int(request.POST.get('quantity', 1))
        
        if quantity > cart_item.book.stock_quantity:
            messages.error(request, 'Không đủ hàng trong kho!')
        elif quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
            messages.success(request, 'Đã cập nhật số lượng!')
        else:
            cart_item.delete()
            messages.success(request, 'Đã xóa sản phẩm khỏi giỏ!')
    
    return redirect('web_cart')


@require_login
def remove_from_cart(request, item_id):
    """Xóa sản phẩm khỏi giỏ"""
    if request.method == 'POST':
        cart_item = get_object_or_404(CartItem, id=item_id)
        cart_item.delete()
        messages.success(request, 'Đã xóa sản phẩm khỏi giỏ hàng!')
    
    return redirect('web_cart')


# ================ CHECKOUT & ORDER VIEWS ================

@require_login
def checkout(request):
    """Trang thanh toán"""
    user, user_type = get_current_user(request)
    if user_type != 'customer':
        messages.error(request, 'Chỉ khách hàng mới có thể thanh toán!')
        return redirect('web_home')
    
    customer = user
    
    cart = get_object_or_404(Cart, customer=customer)
    cart_items = CartItem.objects.filter(cart=cart).select_related('book')
    
    if not cart_items.exists():
        messages.warning(request, 'Giỏ hàng trống!')
        return redirect('web_cart')
    
    subtotal = sum(item.book.price * item.quantity for item in cart_items)
    
    shipping_methods = Shipping.objects.all()
    payment_methods = Payment.objects.all()
    
    context = {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'shipping_methods': shipping_methods,
        'payment_methods': payment_methods,
    }
    return render(request, 'cart/checkout.html', context)


@require_login
def place_order(request):
    """Đặt hàng"""
    if request.method == 'POST':
        user, user_type = get_current_user(request)
        if user_type != 'customer':
            messages.error(request, 'Chỉ khách hàng mới có thể đặt hàng!')
            return redirect('web_home')
        
        customer = user
        
        cart = get_object_or_404(Cart, customer=customer)
        cart_items = CartItem.objects.filter(cart=cart).select_related('book')
        
        if not cart_items.exists():
            messages.error(request, 'Giỏ hàng trống!')
            return redirect('web_cart')
        
        # Get shipping & payment
        shipping_id = request.POST.get('shipping_id')
        payment_id = request.POST.get('payment_id')
        
        shipping = get_object_or_404(Shipping, id=shipping_id)
        payment = get_object_or_404(Payment, id=payment_id)
        
        # Calculate total
        subtotal = sum(Decimal(str(item.book.price)) * item.quantity for item in cart_items)
        total_price = subtotal + shipping.fee
        
        # Create order
        staff = Staff.objects.first()  # Demo: get first staff
        order = Order.objects.create(
            customer=customer,
            staff=staff,
            shipping=shipping,
            payment=payment,
            total_price=total_price,
            status='Pending'
        )
        
        # Create order items & update stock
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                book=item.book,
                quantity=item.quantity
            )
            
            # Update stock
            item.book.stock_quantity -= item.quantity
            item.book.save()
        
        # Clear cart
        cart_items.delete()
        
        messages.success(request, f'Đặt hàng thành công! Mã đơn: #{order.id}')
        return redirect('web_order_detail', order_id=order.id)
    
    return redirect('web_checkout')


@require_login
def order_history(request):
    """Lịch sử đơn hàng"""
    user, user_type = get_current_user(request)
    if user_type != 'customer':
        messages.error(request, 'Chỉ khách hàng mới có lịch sử đơn hàng!')
        return redirect('web_home')
    
    customer = user
    
    orders = Order.objects.filter(
        customer=customer
    ).select_related('shipping', 'payment', 'staff').order_by('-order_date')
    
    context = {
        'orders': orders,
    }
    return render(request, 'order/list.html', context)


@require_login
def order_detail(request, order_id):
    """Chi tiết đơn hàng"""
    user, user_type = get_current_user(request)
    if user_type != 'customer':
        messages.error(request, 'Bạn không có quyền xem đơn hàng này!')
        return redirect('web_home')
    
    customer = user
    
    order = get_object_or_404(
        Order,
        id=order_id,
        customer=customer
    )
    
    order_items = OrderItem.objects.filter(order=order).select_related('book')
    
    context = {
        'order': order,
        'order_items': order_items,
    }
    return render(request, 'order/detail.html', context)


# ================ STAFF VIEWS ================

@require_staff
def staff_dashboard(request):
    """Trang quản lý kho - Staff"""
    books = Book.objects.all().select_related('category').order_by('stock_quantity')
    categories = Category.objects.all()
    
    # Low stock alert
    low_stock = books.filter(stock_quantity__lt=10)
    
    context = {
        'books': books,
        'categories': categories,
        'low_stock': low_stock,
    }
    return render(request, 'staff/dashboard.html', context)


@require_staff
def staff_add_book(request):
    """Thêm sách mới"""
    if request.method == 'POST':
        title = request.POST.get('title')
        author = request.POST.get('author')
        price = request.POST.get('price')
        stock_quantity = request.POST.get('stock_quantity')
        category_id = request.POST.get('category_id')
        
        category = get_object_or_404(Category, id=category_id)
        
        Book.objects.create(
            title=title,
            author=author,
            price=price,
            stock_quantity=stock_quantity,
            category=category
        )
        
        messages.success(request, f'Đã thêm sách "{title}" vào kho!')
        return redirect('web_staff_dashboard')
    
    return redirect('web_staff_dashboard')


@require_staff
def staff_update_stock(request, book_id):
    """Cập nhật số lượng tồn kho"""
    if request.method == 'POST':
        book = get_object_or_404(Book, id=book_id)
        stock_quantity = int(request.POST.get('stock_quantity', 0))
        
        book.stock_quantity = stock_quantity
        book.save()
        
        messages.success(request, f'Đã cập nhật kho cho "{book.title}"')
    
    return redirect('web_staff_dashboard')


@require_staff
def staff_delete_book(request, book_id):
    """Xóa sách"""
    if request.method == 'POST':
        book = get_object_or_404(Book, id=book_id)
        title = book.title
        book.delete()
        
        messages.success(request, f'Đã xóa sách "{title}"')
    
    return redirect('web_staff_dashboard')


# ================ RECOMMENDATION VIEWS ================

@require_login
def recommendation_list(request):
    """Trang gợi ý sách"""
    user, user_type = get_current_user(request)
    if user_type != 'customer':
        messages.error(request, 'Chỉ khách hàng mới có gợi ý sách!')
        return redirect('web_home')
    
    customer_id = user.id
    
    # Top rated books
    top_rated = Book.objects.annotate(
        avg_rating=Avg('rating__score'),
        rating_count=Count('rating')
    ).filter(
        rating_count__gt=0
    ).order_by('-avg_rating')[:8]
    
    # Based on purchase history
    customer = get_object_or_404(Customer, id=customer_id)
    purchased_books = OrderItem.objects.filter(
        order__customer=customer
    ).values_list('book__category_id', flat=True).distinct()
    
    history_based = Book.objects.filter(
        category_id__in=list(purchased_books)
    ).exclude(
        id__in=OrderItem.objects.filter(
            order__customer=customer
        ).values_list('book_id', flat=True)
    ).annotate(
        avg_rating=Avg('rating__score')
    ).order_by('-avg_rating')[:8]
    
    context = {
        'top_rated': top_rated,
        'history_based': history_based,
    }
    return render(request, 'recommendation/list.html', context)
