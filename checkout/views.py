from decimal import Decimal
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from requested_inventory.models import ProductRequest
from myapp.models import UserProfile
from .models import CreditMemoRequest
from .forms import CreditMemoRequestForm

@login_required
def request_credit_memo(request, request_id):
    """View for users to request a credit memo."""
    product_request = get_object_or_404(ProductRequest, id=request_id)

    if request.method == 'POST':
        form = CreditMemoRequestForm(request.POST)
        if form.is_valid():
            # Save the credit memo request
            credit_memo_request = form.save(commit=False)
            credit_memo_request.product_request = product_request
            credit_memo_request.requested_by = request.user
            credit_memo_request.save()
            messages.success(request, 'Your credit memo request has been submitted and is pending approval.')
            return redirect('receipt', product_request_id=request_id)
    else:
        form = CreditMemoRequestForm()

    return render(request, 'inventory/request_credit_memo.html', {
        'form': form,
        'product_request': product_request
    })

@staff_member_required
def manage_credit_memo_requests(request):
    """View for superusers to approve or reject credit memo requests."""
    pending_requests = CreditMemoRequest.objects.filter(status='pending')

    if request.method == 'POST':
        request_id = request.POST.get('request_id')
        action = request.POST.get('action')
        credit_memo = get_object_or_404(CreditMemoRequest, id=request_id)
        product_request = credit_memo.product_request
        user_profile = UserProfile.objects.get(user=credit_memo.requested_by)

        if action == 'approve':
            # Check if there is a new quantity
            if credit_memo.new_quantity is not None:
                original_quantity = product_request.quantity_requested
                new_quantity = credit_memo.new_quantity

                if new_quantity < original_quantity:
                    # Case 1: New quantity is less, refund the difference
                    original_total = Decimal(product_request.product.price) * Decimal(original_quantity)
                    new_total = Decimal(product_request.product.price) * Decimal(new_quantity)

                    # Calculate the difference and refund it to the user's balance
                    refund_amount = original_total - new_total
                    user_profile.balance += refund_amount
                    user_profile.save()

                    # Update the ProductRequest with the new quantity
                    product_request.quantity_requested = new_quantity
                    product_request.save()

                elif new_quantity > original_quantity:
                    # Case 2: New quantity is greater, charge the difference
                    original_total = Decimal(product_request.product.price) * Decimal(original_quantity)
                    new_total = Decimal(product_request.product.price) * Decimal(new_quantity)

                    # Calculate the additional cost
                    additional_cost = new_total - original_total

                    # Check if the user has enough balance to cover the additional cost
                    if user_profile.balance >= additional_cost:
                        # Deduct the additional cost from the user's balance
                        user_profile.balance -= additional_cost
                        user_profile.save()

                        # Update the ProductRequest with the new quantity
                        product_request.quantity_requested = new_quantity
                        product_request.save()
                    else:
                        # Insufficient balance to cover the extra cost
                        messages.error(request, 'Insufficient balance to cover the additional quantity.')
                        return redirect('manage_credit_memo_requests')

            # Mark the credit memo as approved
            credit_memo.status = 'approved'
            credit_memo.approved_at = timezone.now()
            credit_memo.approved_by = request.user
            credit_memo.save()

            messages.success(request, 'Credit memo request approved and balance updated if applicable.')
        elif action == 'reject':
            # Mark the credit memo as rejected
            credit_memo.status = 'rejected'
            credit_memo.save()
            messages.success(request, 'Credit memo request rejected.')

        return redirect('manage_credit_memo_requests')

    return render(request, 'inventory/manage_credit_memo_requests.html', {
        'pending_requests': pending_requests
    })

def process_payment(request, product_request_id):
    """View for processing payments."""
    product_request = get_object_or_404(ProductRequest, id=product_request_id)

    # Calculate costs
    total_cost = Decimal(product_request.product.price) * Decimal(product_request.quantity_requested)
    tax_rate = Decimal('0.001')  # 0.1%
    shipping_fee = Decimal('2.00')  # $2 shipping fee
    tax = total_cost * tax_rate
    total_with_tax_and_shipping = total_cost + tax + shipping_fee

    if request.method == 'POST':
        shipping_address = request.POST.get('shipping_address')
        card_number = request.POST.get('card_number')
        expiry_date = request.POST.get('expiry_date')
        cvv = request.POST.get('cvv')
        currency = request.POST.get('currency')

        # Fetch the user's profile
        user_profile = get_object_or_404(UserProfile, user=request.user)

        # Check if user has enough balance
        if user_profile.balance >= total_with_tax_and_shipping:
            # Deduct the total from the user's balance
            user_profile.balance -= total_with_tax_and_shipping
            user_profile.save()

            # Mark the product request as paid
            product_request.status = 'paid'
            product_request.save()

            # Store the receipt data in the session
            request.session['receipt_data'] = {
                'total_cost': str(total_cost),
                'tax': str(tax),
                'shipping_fee': str(shipping_fee),
                'total_with_tax_and_shipping': str(total_with_tax_and_shipping),
            }

            # Redirect to the receipt view without setting a new message
            return redirect('receipt', product_request_id=product_request_id)
        else:
            # Show error message if balance is insufficient
            messages.error(request, 'Insufficient balance. Please top up your account or use a different payment method.')
            return redirect('checkout', request_id=product_request_id)

    # If it's a GET request, redirect back to the checkout page
    return redirect('checkout', request_id=product_request_id)
def checkout(request, request_id):
    """View for displaying the checkout details."""
    product_request = get_object_or_404(ProductRequest, id=request_id, status='approved')
    user_profile = get_object_or_404(UserProfile, user=request.user)

    # Calculate costs
    total_cost = Decimal(product_request.product.price) * Decimal(product_request.quantity_requested)
    tax_rate = Decimal('0.001')  # 0.1%
    shipping_fee = Decimal('2.00')  # $2 shipping fee
    tax = total_cost * tax_rate
    total_with_tax_and_shipping = total_cost + tax + shipping_fee

    # Calculate adjusted total by deducting user's balance
    balance = user_profile.balance
    adjusted_total = max(total_with_tax_and_shipping - balance, Decimal('0.00'))  # Ensure it doesn't go negative

    # Prepare context for the template
    context = {
        'product_request': product_request,
        'total_cost': total_cost,
        'tax': tax,
        'shipping_fee': shipping_fee,
        'total_with_tax_and_shipping': total_with_tax_and_shipping,
        'balance': balance,
        'adjusted_total': adjusted_total,
        'status': product_request.status,
    }
    return render(request, 'inventory/checkout.html', context)

def receipt_view(request, product_request_id):
    """View for displaying the receipt."""
    product_request = get_object_or_404(ProductRequest, id=product_request_id)

    # Calculate costs for display
    total_cost = Decimal(product_request.product.price) * Decimal(product_request.quantity_requested)
    tax_rate = Decimal('0.001')  # 0.1%
    shipping_fee = Decimal('2.00')  # $2 shipping fee
    tax = total_cost * tax_rate
    total_with_tax_and_shipping = total_cost + tax + shipping_fee

    # Prepare context for receipt
    context = {
        'product_request': product_request,
        'total_cost': total_cost,
        'tax': tax,
        'shipping_fee': shipping_fee,
        'total_with_tax_and_shipping': total_with_tax_and_shipping,
        'user': request.user,
        'user_profile': UserProfile.objects.get(user=request.user)
    }

    return render(request, 'inventory/receipt.html', context)
