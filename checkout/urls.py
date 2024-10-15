from django.urls import path
from . import views

urlpatterns = [
    # Other URL patterns
    path('checkout/<int:request_id>/', views.checkout, name='checkout'),
]
