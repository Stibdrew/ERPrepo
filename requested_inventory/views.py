from django.shortcuts import render

# Create your views here.
def requested_inventory(request):
    return render(request, 'inventory/requested_inventory.html')