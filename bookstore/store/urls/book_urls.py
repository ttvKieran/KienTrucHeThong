from django.urls import path
from store.controllers.bookController import book_views

urlpatterns = [
    path("", book_views.list_books, name="api_list_books"),
    path("<int:book_id>", book_views.get_book_detail, name="api_book_detail"),
]
