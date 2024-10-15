
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import UserProfile
from django.contrib.auth.models import User

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    company_name = forms.CharField(max_length=100, required=True, label='Company Name')
    full_name = forms.CharField(max_length=100, required=True, label='Full Name')
    mobile_number = forms.CharField(max_length=15, required=True, label='Mobile Number')
    business_title = forms.CharField(max_length=100, required=True, label='Business Title')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'company_name', 'full_name', 'mobile_number', 'business_title']


class UserProfileEditForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['full_name', 'company_name', 'mobile_number', 'business_title']
