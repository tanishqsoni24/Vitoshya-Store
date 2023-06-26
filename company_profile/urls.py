from django.urls import path, include  
from . import views 

urlpatterns = [
    path('',views.index, name="home"),
    path("cart", views.cart, name="cart"),
    path('saveNewsLetter', views.saveNewsLetter, name="saveNewsLetter"),
    path('contact', views.contact, name="contact")
]