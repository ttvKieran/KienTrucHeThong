from django.urls import path
from store.controllers.orderController import cart_views

urlpatterns = [
    path("", cart_views.view_cart, name="api_view_cart"),
    path("add", cart_views.add_to_cart, name="api_add_to_cart"),
    path("item/<int:item_id>", cart_views.manage_cart_item, name="api_manage_cart_item"),
]
