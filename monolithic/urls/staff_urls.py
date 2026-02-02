from django.urls import path
from controllers import staffController, bookController

urlpatterns = [
    # Quản lý nhân viên
    path('', staffController.list_staff, name='list_staff'),
    path('<int:staff_id>/', staffController.get_staff, name='get_staff'),
    
    # Nhân viên quản lý sách (moved to bookController)
    path('books/add/', bookController.add_book_to_inventory, name='add_book_to_inventory'),
    path('books/<int:book_id>/update/', bookController.update_book, name='update_book'),
    path('books/<int:book_id>/stock/', bookController.update_book_stock, name='update_book_stock'),
    path('books/<int:book_id>/delete/', bookController.delete_book, name='delete_book'),
]