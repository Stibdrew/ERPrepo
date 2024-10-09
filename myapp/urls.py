from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),  # Home page
    path('register/', views.register, name='register'),  # Registration page
    path('profile/', views.profile, name='profile'),  # Profile page
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),  # Login page
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),  # Logout page

    path('homepage/', views.homepage, name='homepage'), # Home page
    path('inventory/', views.inventory, name='inventory'), # Profile page
    path('sales/', views.sales, name='sales'), # Profile page

    path('finance/', views.finance, name='finance'), # Profile page
    path('HR/', views.HR, name='HR'), # Profile page



]


