from django.urls import path
from . import views 

urlpatterns = [
    path('', views.index, name="shop"),
    path('product/<str:slug>', views.product, name="product"),
    path("add-to-cart/<str:uid>", views.addToCart, name="cartAdd"),
    path("update-cart", views.updateCart, name="cartUpdate"),
]