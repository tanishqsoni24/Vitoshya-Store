from django.urls import path, include  
from . import views 

urlpatterns = [
    path('login',views.login, name="shop"),
    path('register',views.signup, name="register"),
    path('logout',views.logout, name="logout"),
    path('activate/<email_token>',views.activate_email, name="activate_email"),
]