from decimal import Decimal
from django.shortcuts import render, get_object_or_404
from requested_inventory.models import ProductRequest

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

        # Redirect to a receipt or confirmation page
        return redirect('receipt', product_request_id=product_request.id)

    # Pass all necessary context variables to the template
    context = {
        'product_request': product_request,
        'total_cost': total_cost,
        'tax': tax,
        'shipping_fee': shipping_fee,
        'total_with_tax_and_shipping': total_with_tax_and_shipping,
    }
    return render(request, 'inventory/checkout.html', context)
