from django.urls import path
from store.controllers.customerController import auth_views

urlpatterns = [
    path("register", auth_views.register, name="api_register"),
    path("login", auth_views.user_login, name="api_login"),
    path("logout", auth_views.user_logout, name="api_logout"),
    path("profile", auth_views.get_user_profile, name="api_profile"),
]
