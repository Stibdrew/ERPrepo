from django.http import JsonResponse
from .models import Request
from django.views.decorators.csrf import csrf_exempt
import json
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
import logging
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Request

@login_required
def approve_request(request, request_id):
    req = get_object_or_404(Request, id=request_id)
    req.status = 'approved'  # Set the status to approved
    req.save()
    return redirect('homepage')  # Redirect after approval

@login_required
def decline_request(request, request_id):
    req = get_object_or_404(Request, id=request_id)
    req.status = 'declined'  # Set the status to declined
    req.save()
    return redirect('homepage')  # Redirect after declining


# Set up logging
logger = logging.getLogger(__name__)

@login_required
def delete_request(request, request_id):
    # Get the request object or return a 404 if it doesn't exist
    req = get_object_or_404(Request, id=request_id, user=request.user)

    # Delete the request
    req.delete()

    # Redirect to the homepage or another page after deletion
    return redirect('homepage')


@csrf_exempt  # Use CSRF protection as needed
def submit_request(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        item_name = data.get('item')

        if item_name:
            # Create the request object with status set to 'pending'
            request_obj = Request.objects.create(user=request.user, item=item_name, status='pending')
            return JsonResponse({
                'status': 'success',
                'item': item_name,
                'date': request_obj.created_at.strftime('%Y-%m-%d %H:%M:%S')
            })
        return JsonResponse({'status': 'error', 'message': 'Item name is required.'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})
def homepage_view(request):
    if request.user.is_authenticated:
        # Get requests made by the authenticated user
        user_requests = Request.objects.filter(user=request.user)
        logger.info(f"User requests: {user_requests}")  # Log requests
    else:
        user_requests = []

    return render(request, 'users/homepage.html', {'requests': user_requests})
