from django.shortcuts import render


def home(request):
    """Home page"""
    return render(request, 'bookstore/home.html')


def login_page(request):
    """Login page"""
    return render(request, 'bookstore/login.html')


def register_page(request):
    """Register page"""
    return render(request, 'bookstore/register.html')


def books_page(request):
    """Books catalog page"""
    return render(request, 'bookstore/books.html')


def cart_page(request):
    """Shopping cart page"""
    return render(request, 'bookstore/cart.html')


def profile_page(request):
    """User profile page"""
    return render(request, 'bookstore/profile.html')
