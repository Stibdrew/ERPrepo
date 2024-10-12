from django.urls import path
from .views import submit_request
from .views import homepage_view
from .views import delete_request
from django.urls import path
from .views import approve_request, decline_request
urlpatterns = [
    # ... other URL patterns ...
    path('submit_request/', submit_request, name='submit_request'),
    path('homepage/', homepage_view, name='homepage'),
    path('delete_request/<int:request_id>/', delete_request, name='delete_request'),
    path('approve_request/<int:request_id>/', approve_request, name='approve_request'),
    path('decline_request/<int:request_id>/', decline_request, name='decline_request'),

    # other paths...


]
