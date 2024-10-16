from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserRegisterForm, UserProfileEditForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import UserProfile
from django.contrib.auth.models import User

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
            return redirect('profile')
    else:
        form = UserProfileEditForm(instance=user_profile)

    return render(request, 'users/profile.html', {
        'user': request.user,
        'user_profile': user_profile,
        'balance': user_profile.balance,  # Pass the balance to the template
        'form': form
    })

def inventory(request):
    return render(request, 'users/inventory.html')

def show_all_users(request):
    users = User.objects.all()
    user_profiles = UserProfile.objects.all()

    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        new_balance = request.POST.get(f'balance_{user_id}')

        if user_id and new_balance:
            try:
                # Get the user profile based on the user ID
                user_profile = get_object_or_404(UserProfile, user_id=user_id)
                user_profile.balance = float(new_balance)
                user_profile.save()
                messages.success(request, f'Balance for {user_profile.full_name} updated successfully!')
            except ValueError:
                messages.error(request, 'Please enter a valid number for the balance.')

        # Always redirect after processing POST to avoid re-submission issues
        return redirect('show_all_users')

    # Render the template for GET requests or after POST redirects
    return render(request, 'inventory/show_all_users.html', {
        'users': users,
        'user_profiles': user_profiles
    })
