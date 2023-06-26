from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from shop.models import *
from django.db.models import F, Q, Sum

# Create your views here.

def index(request):
    Categories = Category.objects.all()
    products = Product.objects.all()[:4]
    return render(request, "index/index.html", {'products': products, 'category': Categories})

def contact(request):
    return render(request, "index/contact.html")

@login_required()
def cart(request):
    xart = request.user.cart_set.all()
    total = xart.aggregate(total_price=Sum(F('quantity') * F('product__price')))['total_price']
    return render(request, "index/checkout.html", {'cart': xart, 'total': total})


def saveNewsLetter(request):
    if request.method == "POST":
        email = request.POST.get("email")
        if email:
            news = Newsletter(email=email)
            news.save()
            return redirect("home")
    return redirect("home")