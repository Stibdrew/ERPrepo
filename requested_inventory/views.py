from .models import ProductRequest, Product, StockMovement
from .forms import ProductForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from django.views.decorators.http import require_POST
from .models import Product  # Adjust the import based on your app structure
from django.http import HttpResponseBadRequest

def cancel_request(request, pk):
    request_obj = ProductRequest.objects.get(pk=pk)
    request_obj.delete()
    messages.success(request, 'Request cancelled successfully.')
    return redirect('view_requested_products')
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    return redirect('requested_inventory')  # Redirect to the product list page
@login_required
@require_POST
def update_product(request, product_id):
    product = Product.objects.get(id=product_id)

    if request.method == 'POST':
        name = request.POST.get('name')
        sku = request.POST.get('sku')
        price = request.POST.get('price')
        description = request.POST.get('description')


        # Check for missing fields
        if not name or not sku or price is None:
            # Return an error message or redirect back with an error
            return render(request, 'inventory/requested_inventory.html', {
                'product': product,
                'error': 'Please fill in all fields.',
            })

        # Update product details
        product.name = name
        product.sku = sku
        product.price = price
        product.description = description
        product.save()
        return redirect('requested_inventory')  # or wherever you want to redirect

    return render(request, 'inventory/requested_inventory.html', {'product': product})


@login_required
def delete_product_view(request):
    products = Product.objects.all()  # Fetch all products to display

    return render(request, 'inventory/delete_product.html', {
        'products': products
    })
@login_required
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    messages.success(request, "Product deleted successfully.")
    return redirect('requested_inventory')  # Adjust redirect as needed


@login_required
def delete_product_request(request, request_id):
    product_request = get_object_or_404(ProductRequest, id=request_id)
    product_request.delete()  # Delete the product request
    messages.success(request, "Product request deleted successfully.")
    return redirect('all_products_request')



@login_required
def requested_inventory(request):
    # Fetch all products
    products = Product.objects.all()  # Get all available products

    return render(request, 'inventory/requested_inventory.html', {
        'products': products
    })

@login_required
def approve_request(request, request_id):
    product_request = get_object_or_404(ProductRequest, id=request_id)

    # Fetch the product related to the request
    product = product_request.product

    # Check if the requested quantity can be fulfilled
    if product_request.quantity_requested <= product.quantity:
        # Update the product quantity
        product.quantity -= product_request.quantity_requested
        product.save()  # Save the updated product

        # Update the request status
        product_request.status = 'approved'
        product_request.save()

        messages.success(request, "Product request approved successfully!")
    else:
        messages.error(request, "Cannot approve request. Not enough stock available.")

    return redirect('all_product_requests')  # Redirect to the all products page

@login_required
def decline_request(request, request_id):
    product_request = get_object_or_404(ProductRequest, id=request_id)
    product_request.status = 'declined'
    product_request.save()
    messages.success(request, "Product request declined successfully!")
    return redirect('all_product_requests')  # Redirect to the all products page

@login_required
def add_product_request(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_name')  # Use product ID instead of name
        quantity = request.POST.get('quantity')

        # Fetch the product using the ID
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            messages.error(request, "Product not found.")
            return redirect('add_product_request')

        # Create a new product request
        ProductRequest.objects.create(
            user=request.user,
            product=product,  # Use the product instance here
            quantity_requested=quantity  # Use the correct field name here
        )

        messages.success(request, "Product request submitted successfully.")
        return redirect('homepage')  # Redirect to a success page or another view

    # Fetch all products to display in the dropdown and existing products
    products = Product.objects.all()  # Fetch all products
    return render(request, 'inventory/add_product_request.html', {
        'products': products,  # Pass existing products to the template
        'form': ProductForm()   # Pass the form instance to the template
    })

@login_required
def view_requested_products(request):
    # Fetch requested products for the logged-in user
    requested_products = ProductRequest.objects.filter(user=request.user)

    return render(request, 'inventory/view_requested_products.html', {
        'requested_products': requested_products
    })

@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Product added successfully!")
            return redirect('add_product')  # Redirect to your inventory page
    else:
        form = ProductForm()

    return render(request, 'inventory/add_product.html', {'form': form})

@login_required
def adjust_stock(request, product_id, quantity, movement_type):
    product = get_object_or_404(Product, id=product_id)

    if movement_type == 'IN':
        product.quantity += quantity
    elif movement_type == 'OUT':
        product.quantity -= quantity

    # Save the stock movement
    StockMovement.objects.create(
        product=product,
        quantity=quantity,
        movement_type=movement_type
    )
    product.save()

    return redirect('requested_inventory')
@login_required
def update_stock(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        stock_change = int(request.POST.get('stock_change', 0))
        product.quantity += stock_change  # Update stock quantity
        product.save()  # Save the changes
        messages.success(request, "Stock updated successfully!")
        return redirect('requested_inventory')  # Redirect back to the product list


@login_required
def all_product_requests(request):
    requested_products = ProductRequest.objects.all()  # Or filter based on the user
    return render(request, 'inventory/all_product_requests.html', {'requested_products': requested_products})



@login_required
def all_product_requests(request):
    requested_products = ProductRequest.objects.all()  # Or filter based on the user
    return render(request, 'inventory/all_product_requests.html', {'requested_products': requested_products})
