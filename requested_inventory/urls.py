
from django.urls import path
from .views import requested_inventory, add_product_request, add_product, view_requested_products , all_product_requests, approve_request, decline_request
from .views import delete_product_request, all_products, delete_product, delete_product_view, edit_product
urlpatterns = [

    # ... other URL patterns ...
    path('requested_inventory/', requested_inventory, name='requested_inventory'),
    path('add-product-request/', add_product_request, name='add_product_request'),
    path('add-product/', add_product, name='add_product'),
    path('requested-products/', view_requested_products, name='view_requested_products'),
    path('all-products-request/', all_product_requests, name='all_products_request'),
    path('approve-request/<int:request_id>/', approve_request, name='approve_request'),
    path('decline-request/<int:request_id>/', decline_request, name='decline_request'),
    path('product-requests/delete/<int:request_id>/', delete_product_request, name='delete_product_request'),
    path('all-product/', all_products, name='all_products'),
    path('products/delete/<int:product_id>/', delete_product, name='delete_product'),
    path('products/delete/', delete_product_view, name='delete_product_view'),  # View to display products
    path('edit_product/', edit_product, name='edit_product'),  # Add this line

]

