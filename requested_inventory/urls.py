
from django.urls import path
from .views import requested_inventory
urlpatterns = [
    # ... other URL patterns ...
    path('requested_inventory/', requested_inventory, name='requested_inventory'),


]

