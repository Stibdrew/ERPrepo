from django.db import models
from django.contrib.auth.models import User

class ProductRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=100)
    quantity = models.IntegerField()
    date_requested = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.product_name} requested by {self.user.username}"
