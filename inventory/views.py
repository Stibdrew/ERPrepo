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
    logger.info(f"Approving request with ID: {request_id}")  # Log the request ID
    try:
        req = Request.objects.get(id=request_id, status='pending')
        req.status = 'approved'
        req.save()
        return JsonResponse({'status': 'success', 'message': 'Request approved successfully!'})
    except Request.DoesNotExist:
        logger.error(f"Request with ID {request_id} not found.")
        return JsonResponse({'status': 'error', 'message': 'Request not found.'})

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
    user_request = get_object_or_404(Request, id=request_id)

    # Allow deletion if the user is a superuser
    if request.user.is_superuser:
        user_request.delete()  # Delete the request

    return redirect('admin_page')  # Redirect to a relevant page after deletio

logger = logging.getLogger(__name__)

import json
import logging
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Request  # Ensure your Request model is imported

# Set up logging
logger = logging.getLogger(__name__)

@login_required
def submit_request(request):
    if request.method == 'POST':
        try:
            # Parse JSON data
            data = json.loads(request.body)
            item = data.get('item')

            # Check if the user already has a pending or approved request
            existing_request_approved = Request.objects.filter(user=request.user, status='approved').exists()
            existing_request_pending = Request.objects.filter(user=request.user, status='pending').exists()

            if existing_request_approved or existing_request_pending:
                return JsonResponse({'status': 'error', 'message': 'You already have a pending or approved request.'})

            # Create a new request
            new_request = Request(user=request.user, item=item)
            new_request.save()

            return JsonResponse({
                'status': 'success',
                'item': item,
                'date': new_request.created_at.strftime("%Y-%m-%d %H:%M:%S")
            })
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON data.'})
        except Exception as e:
            logger.error(f"Error in submit_request: {str(e)}")
            return JsonResponse({'status': 'error', 'message': 'An error occurred.'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})


@login_required
def homepage_view(request):
    # Get requests made by the authenticated user
    user_requests = Request.objects.filter(user=request.user)
    logger.info(f"User requests: {user_requests}")  # Log requests

    # Count approved requests
    approved_requests_count = user_requests.filter(status='approved').count()

    return render(request, 'users/homepage.html', {
        'requests': user_requests,
        'approved_requests_count': approved_requests_count,
    })

@login_required
def requested_inventory(request):
    return render(request, 'inventory/requested_inventory.html')