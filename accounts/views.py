from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import login as auth_login
from django.http import HttpResponse
from .models import Profile
import re

# Create your views here.

def login(request):
    if request.method == "POST":
        username = request.POST.get('Username')
        password = request.POST.get('Password')

        user_obj = User.objects.filter(username=username)
        if not user_obj.exists():
            messages.warning(request, "Account doesn't exists")
            return redirect("/accounts/login")

        if not user_obj[0].profile.is_email_verified:
            messages.warning(request, "Your email is not verified")
            return redirect("/accounts/login")

        user_obj = authenticate(username=username, password=password)
        if user_obj:
            auth_login(request, user_obj)
            return redirect("/shop")

        messages.warning(request, "Invalid Credentials")
        return redirect("/accounts/login")
    return render(request, "accounts/login.html")

def signup(request):
    if(request.method=="POST"):
        full_Name = request.POST.get('full_name')
        first_name, last_name = full_Name.split(' ', 1) if " " in full_Name else (full_Name, "")
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        punctuations = '''!()-[]{};:'""\,<>./?@#$%^&*~'''
        email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'

        if punctuations in username:
            messages.warning(request, "Username cannot contain special characters only alphabets, numbers and underscore(_) are allowed")
            return redirect("/accounts/register")

        if username == "":
            messages.warning(request, "Username cannot be empty")
            return redirect("/accounts/register")

        if len(password) < 8:
            messages.warning(request, "Password must be atleast 8 characters long")
            return redirect("/accounts/register")

        if f"{first_name} {last_name}" in password:
            messages.warning(request, "Password cannot contain your name")
            return redirect("/accounts/register")

        if not re.fullmatch(email_regex, email):
            messages.warning(request, "Invalid Email")
            return redirect("/accounts/register")

        if User.objects.filter(email=email).exists():
            messages.warning(request, "Email already exists")
            return redirect("/accounts/register")

        user_obj = User.objects.filter(username=username)
        if user_obj.exists():
            messages.warning(request, f"Username already exists! Please try another username, Eg: {username}_123__, {full_Name[0]}_1234__")
            return redirect("/accounts/register")
        user_obj = User.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name)
        user_obj.set_password(password)

        user_obj.save()

        messages.success(request, "An Email has been sent to your registered mail id")
        return redirect("/accounts/register")
    return render(request, "accounts/signup.html")

def activate_email(request, email_token):
    try:
        user = Profile.objects.get(email_token=email_token)
        user.is_email_verified = True
        user.email_token = ''
        user.save()
        messages.success(request, "Email Verified Successfully, Please Login to continue")
        return redirect("/accounts/login")
    except Exception as e:
        return HttpResponse("Invalid Email Token")

def logout(request):
    auth_logout(request)
    messages.success(request, "Logged Out Successfully")
    return redirect("/accounts/login")