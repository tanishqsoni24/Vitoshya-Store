from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib import messages
from shop.models import *
from .models import *
from django.db.models import F, Q, Sum
import re

# Create your views here.

def index(request):
    Categories = Category.objects.all()
    products = Product.objects.all()[:4]
    return render(request, "index/index.html", {'products': products, 'category': Categories, 'home': True})

def contact(request):
    Categories = Category.objects.all()
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")
        email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
        if name and email and message:
            if not re.fullmatch(email_regex, email):
                messages.warning(request, "Invalid Email")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            contact = Contact(name=name, email=email, message=message)
            contact.save()
            messages.success(request, "Your message has been sent successfully")
            return redirect("/contact")
        else:
            messages.warning(request, "Please fill all the fields")
            return redirect("/contact")
    return render(request, "index/contact.html", {'category': Categories})

@login_required()
def cart(request):
    xart = request.user.cart_set.all()
    Categories = Category.objects.all()
    total = xart.aggregate(total_price=Sum(F('quantity') * F('product__price')))['total_price']
    return render(request, "index/checkout.html", {'cart': xart, 'total': total, 'category': Categories})


def saveNewsLetter(request):
    if request.method == "POST":
        email = request.POST.get("email")
        email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
        if email:
            if not re.fullmatch(email_regex, email):
                messages.warning(request, "Invalid Email")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            news = Newsletter(email=email)
            news.save()
            messages.success(request, "Your email has been added to our newsletter")
            return redirect("home")
        else:
            messages.warning(request, "Empty fields are not acceptable")
            return redirect("home")
    return redirect("home")