from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('register/', views.register, name="register"), 
    path('login/', views.loginPage, name="login"), 
    path('search/', views.search, name="search"), 
     path('category/', views.category, name="category"), 
    path('logout/', views.logoutPage, name="logout"), 
    path('cart/', views.cart, name="cart"), 
    path('checkout/', views.checkout, name="checkout"),
     path('update_item/', views.updateItem, name="update_item"),
]
