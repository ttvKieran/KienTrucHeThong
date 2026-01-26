from django.urls import path
from controllers import staffController

urlpatterns = [
    # Quản lý nhân viên
    path('', staffController.list_staff, name='list_staff'),
    path('<int:staff_id>/', staffController.get_staff, name='get_staff'),
    
    # Nhân viên nhập sách vào kho
    path('books/add/', staffController.add_book_to_inventory, name='add_book_to_inventory'),
    path('books/<int:book_id>/update/', staffController.update_book, name='update_book'),
    path('books/<int:book_id>/stock/', staffController.update_book_stock, name='update_book_stock'),
    path('books/<int:book_id>/delete/', staffController.delete_book, name='delete_book'),
]