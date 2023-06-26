from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect
from .models import *
import json


# Create your views here.
def index(request):
    Categories = Category.objects.all()
    products = Product.objects.all()
    recent_products = list(Product.objects.all().order_by('-created_at')[:2])
    return render(request, "shop/products.html", {'products': products, 'category': Categories, 'recent_products':recent_products})


def product(request, slug):
    prod = Product.objects.get(slug=slug)
    return render(request, "shop/product-single.html", {'product': prod})


@login_required(login_url='/accounts/login')
def addToCart(request, uid):
    prod = Product.objects.filter(uid=uid).first()
    if prod:
        cart = Cart.objects.filter(account=request.user, product=prod).first()
        if cart:
            cart.quantity += 1
            cart.save()
        else:
            cart = Cart(account=request.user, product=prod, quantity=1)
            cart.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def updateCart(request):
    if request.method == "POST":
        json_data = json.loads(request.POST.get('cart'))

        for data in json_data:
            uid = data.get("uid")
            qty = data.get("quantity")
            xart = Cart.objects.filter(id=uid).first()
            if xart:
                xart.quantity = qty
                xart.save()

        return HttpResponse("success")

