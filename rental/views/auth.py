from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model
from rental.forms.auth import UserSignupForm, UserLoginForm, UserProfileForm, ChangePasswordForm
from rental.models.booking import Booking
from rental.models.wishlist import Wishlist

User = get_user_model()

def signup_view(request):
    """
    Handles user signup and auto-logs in the user upon successful creation.
    """
    if request.user.is_authenticated:
        return redirect('dashboard')
        
    if request.method == 'POST':
        form = UserSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Welcome to DriveEase, {user.first_name}! Your account has been created.")
            return redirect('dashboard')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")
    else:
        form = UserSignupForm()
    return render(request, 'auth/signup.html', {'form': form})

def login_view(request):
    """
    Handles user login. Supports username or email authentication.
    """
    if request.user.is_authenticated:
        return redirect('dashboard')
        
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username_or_email = form.cleaned_data.get('username_or_email')
            password = form.cleaned_data.get('password')
            remember_me = form.cleaned_data.get('remember_me')
            
            # Resolve username if email was provided
            username = username_or_email
            if '@' in username_or_email:
                try:
                    user_obj = User.objects.get(email=username_or_email)
                    username = user_obj.username
                except User.DoesNotExist:
                    pass
            
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                if not remember_me:
                    request.session.set_expiry(0) # Session expires when browser closes
                messages.success(request, f"Welcome back, {user.first_name or user.username}!")
                return redirect('dashboard')
            else:
                messages.error(request, "Invalid username/email or password.")
    else:
        form = UserLoginForm()
    return render(request, 'auth/login.html', {'form': form})

def logout_view(request):
    """
    Handles user logout.
    """
    logout(request)
    messages.info(request, "You have successfully logged out of DriveEase.")
    return redirect('home')

def forgot_password_view(request):
    """
    Requests username or email and simulates a password reset link shown as a message.
    """
    if request.method == 'POST':
        email_or_username = request.POST.get('email_or_username')
        user = None
        if '@' in email_or_username:
            user = User.objects.filter(email=email_or_username).first()
        else:
            user = User.objects.filter(username=email_or_username).first()
            
        if user:
            reset_url = request.build_absolute_uri(f"/reset-password/{user.id}/")
            # In a real app, send email. Here, we present it in a simulation message.
            messages.success(request, f"Simulated Email Sent! Click the link to reset: {reset_url}", extra_tags="reset_link")
            return render(request, 'auth/forgot_password.html', {'success': True, 'reset_url': reset_url})
        else:
            messages.error(request, "No account was found with that username or email.")
            
    return render(request, 'auth/forgot_password.html')

def reset_password_view(request, user_id):
    """
    Allows user to reset their password using the simulated reset URL.
    """
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        new_password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        if len(new_password) < 8:
            messages.error(request, "Password must be at least 8 characters long.")
        elif new_password != confirm_password:
            messages.error(request, "Passwords do not match.")
        else:
            user.set_password(new_password)
            user.save()
            messages.success(request, "Your password has been successfully reset. Please log in.")
            return redirect('login')
            
    return render(request, 'auth/reset_password.html', {'reset_user': user})

@login_required
def dashboard_view(request):
    """
    Renders the User Dashboard: list of bookings, wishlist cars, recent reviews, etc.
    """
    bookings = Booking.objects.filter(user=request.user).order_by('-created_at')
    wishlist_item, created = Wishlist.objects.get_or_create(user=request.user)
    favorite_cars = wishlist_item.cars.all()
    
    context = {
        'bookings': bookings,
        'favorite_cars': favorite_cars,
        'current_bookings': bookings.filter(status__in=['Pending', 'Confirmed'])[:3]
    }
    return render(request, 'dashboard/index.html', context)

@login_required
def edit_profile_view(request):
    """
    Allows the logged-in user to edit their profile and upload a profile picture.
    """
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated successfully.")
            return redirect('dashboard')
        else:
            messages.error(request, "Failed to update profile. Check the errors below.")
    else:
        form = UserProfileForm(instance=request.user)
        
    return render(request, 'dashboard/profile.html', {'form': form})

@login_required
def change_password_view(request):
    """
    Allows the logged-in user to change their account password.
    """
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            user = request.user
            old_password = form.cleaned_data['old_password']
            new_password = form.cleaned_data['new_password']
            
            if not user.check_password(old_password):
                messages.error(request, "Your current password was entered incorrectly.")
            else:
                user.set_password(new_password)
                user.save()
                update_session_auth_hash(request, user) # Keeps user logged in
                messages.success(request, "Your password was successfully updated.")
                return redirect('dashboard')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")
    else:
        form = ChangePasswordForm()
        
    return render(request, 'dashboard/change_password.html', {'form': form})
