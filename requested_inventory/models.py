from django.contrib.auth.models import User
from django.db import models
from django.conf import settings

class Product(models.Model):
    name = models.CharField(max_length=255)
    sku = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    company_name = models.CharField(max_length=255, default="Unknown Company")  # Set a default value

    def __str__(self):
        return self.name


class ProductRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('declined', 'Declined'),
        ('paid', 'Paid'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity_requested = models.IntegerField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    company_name = models.CharField(max_length=255, blank=True)  # New field to store company name

    def __str__(self):
        return f"{self.user.username} from {self.company_name} requested {self.product.name} (Qty: {self.quantity_requested})"

    def get_total_cost(self):
        return self.product.price * self.quantity_requested

    def save(self, *args, **kwargs):
        # Automatically populate the company_name field based on the user's profile
        if not self.company_name:
            self.company_name = self.user.userprofile.company_name  # Fetch company name from UserProfile
        super().save(*args, **kwargs)


class StockMovement(models.Model):
    MOVEMENT_TYPE_CHOICES = [
        ('IN', 'Stock In'),
        ('OUT', 'Stock Out'),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    movement_type = models.CharField(max_length=3, choices=MOVEMENT_TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.movement_type} - {self.product.name} ({self.quantity})"
