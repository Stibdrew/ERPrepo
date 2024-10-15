from decimal import Decimal
from django.shortcuts import render, get_object_or_404, redirect
from requested_inventory.models import ProductRequest
from myapp.models import UserProfile  # Adjust if necessary

def checkout(request, request_id):
    product_request = get_object_or_404(ProductRequest, id=request_id, status='approved')
    total_cost = Decimal(product_request.product.price) * Decimal(product_request.quantity_requested)
    tax_rate = Decimal('0.001')  # 0.1%
    shipping_fee = Decimal('2.00')  # $2 shipping fee
    tax = total_cost * tax_rate
    total_with_tax_and_shipping = total_cost + tax + shipping_fee

    context = {
        'product_request': product_request,
        'total_cost': total_cost,
        'tax': tax,
        'shipping_fee': shipping_fee,
        'total_with_tax_and_shipping': total_with_tax_and_shipping,
        'status': product_request.status,
    }
    return render(request, 'inventory/checkout.html', context)


def process_payment(request, product_request_id):
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

        # TODO: Add payment gateway integration here

        # Change the status to 'Paid'
        product_request.status = 'paid'  # Ensure this status exists in your model
        product_request.save()

        # Store the receipt data in the session
        request.session['receipt_data'] = {
            'total_cost': str(total_cost),
            'tax': str(tax),
            'shipping_fee': str(shipping_fee),
            'total_with_tax_and_shipping': str(total_with_tax_and_shipping),
        }

        # Redirect to the receipt view
        return redirect('receipt', product_request_id=product_request_id)

    # If it's a GET request, redirect back to the checkout page
    return redirect('checkout', request_id=product_request_id)


def receipt_view(request, product_request_id):
    product_request = get_object_or_404(ProductRequest, id=product_request_id)

    # Ensure that all necessary values are calculated and passed
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
        'user_profile': UserProfile.objects.get(user=request.user)  # Ensure this matches your UserProfile model
    }

    return render(request, 'inventory/receipt.html', context)

