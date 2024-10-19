
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import UserProfile
from django.contrib.auth.models import User


class CashInForm(forms.Form):
    amount = forms.DecimalField(max_digits=10, decimal_places=2, required=True, min_value=0.01, label='Amount to Add')

    # Adding payment details
    card_number = forms.CharField(
        max_length=16,
        min_length=16,
        required=True,
        label='Card Number',
        widget=forms.TextInput(attrs={'placeholder': '1234 5678 9012 3456'})
    )
    card_expiry = forms.CharField(
        max_length=5,
        required=True,
        label='Expiry Date (MM/YY)',
        widget=forms.TextInput(attrs={'placeholder': 'MM/YY'})
    )
    card_cvv = forms.CharField(
        max_length=3,
        min_length=3,
        required=True,
        label='CVV',
        widget=forms.PasswordInput(attrs={'placeholder': '123'})
    )

class UserProfileEditForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['full_name', 'company_name', 'mobile_number', 'business_title']
