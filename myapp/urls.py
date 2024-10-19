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
    path('edit_profile/', views.edit_profile, name='edit_profile'),  # Add this line
    path('show_all_users/', views.show_all_users, name='show_all_users'),
    path('users/terminate/<int:user_id>/', views.terminate_account, name='terminate_account'),  # Add this line

]


