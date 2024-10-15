from django.urls import path
from . import views

urlpatterns = [
    # Other URL patterns
    path('checkout/<int:request_id>/', views.checkout, name='checkout'),
    path('process_payment/<int:product_request_id>/', views.process_payment, name='process_payment'),
path('checkout/receipt/<int:product_request_id>/', views.receipt_view, name='receipt'),


]
