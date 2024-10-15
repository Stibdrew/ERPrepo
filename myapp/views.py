from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import UserRegisterForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import UserProfile
from .forms import UserProfileEditForm
@login_required()
def edit_profile(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = UserProfileEditForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')  # Redirect to the profile page after saving
    else:
        form = UserProfileEditForm(instance=user_profile)

    return render(request, 'users/profile.html', {'form': form})

def home(request):
    return render(request, 'users/home.html')


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the user first
            # Create a UserProfile instance for the newly registered user with the form data
            UserProfile.objects.create(
                user=user,
                company_name=form.cleaned_data['company_name'],
                full_name=form.cleaned_data['full_name'],
                mobile_number=form.cleaned_data['mobile_number'],
                business_title=form.cleaned_data['business_title']
            )
            messages.success(request, 'Your account has been created! You can now log in.')
            return redirect('login')  # Redirect to login or another page after registration
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

def homepage(request):
    return render(request, 'users/homepage.html')

@login_required()
def profile(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = UserProfileEditForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')  # Redirect to the profile page after saving
    else:
        form = UserProfileEditForm(instance=user_profile)

    return render(request, 'users/profile.html', {
        'user': request.user,
        'user_profile': user_profile,
        'form': form  # Pass the form to the template
    })

def inventory(request):
    return render(request, 'users/inventory.html')


