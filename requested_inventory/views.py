from .models import ProductRequest, Product, StockMovement
from .forms import ProductForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Product


@login_required
def delete_product_view(request):
    products = Product.objects.all()  # Fetch all products to display

    return render(request, 'inventory/delete_product.html', {
        'products': products
    })
@login_required
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.delete()  # Delete the product
    messages.success(request, "Product deleted successfully.")
    return redirect('add_product')  # Redirect to the inventory page or wherever you want


@login_required
def delete_product_request(request, request_id):
    product_request = get_object_or_404(ProductRequest, id=request_id)
    product_request.delete()  # Delete the product request
    messages.success(request, "Product request deleted successfully.")
    return redirect('all_products')  # Ensure this matches your urls.py



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
    product_request.status = 'approved'
    product_request.save()
    messages.success(request, "Product request approved successfully!")
    return redirect('all_products')  # Redirect to the all products page

@login_required
def decline_request(request, request_id):
    product_request = get_object_or_404(ProductRequest, id=request_id)
    product_request.status = 'declined'
    product_request.save()
    messages.success(request, "Product request declined successfully!")
    return redirect('all_products')  # Redirect to the all products page

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
def all_product_requests(request):
    requested_products = ProductRequest.objects.all()  # Or filter based on the user
    return render(request, 'inventory/all_products.html', {'requested_products': requested_products})

def all_products(request):
    products = Product.objects.all()
    return render(request, 'inventory/all_products.html', {'products': products})

def edit_product(request):
    products = Product.objects.all()
    return render(request, 'inventory/edit_products.html', {'products': products})