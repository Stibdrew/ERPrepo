from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from inventory.models import Request  # Replace 'your_app_name' with the actual name of the app where the Request model is defined

# Check if the user is an admin
def is_admin(user):
    return user.is_superuser

@user_passes_test(is_admin)
def admin_page(request):
    all_requests = Request.objects.all().order_by('-created_at')  # Fetch all requests
    context = {
        'requests': all_requests,
    }
    return render(request, 'users/admin_page.html', context)
