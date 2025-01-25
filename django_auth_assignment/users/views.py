

# Create your views here.


from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CustomLoginForm

def custom_login(request):
    if request.method == 'POST':
        form = CustomLoginForm(request.POST)
        if form.is_valid():
            username_or_email = form.cleaned_data['username_or_email']
            password = form.cleaned_data['password']

            # Check if the input is an email or username
            print(f"Attempting to login with username/email: {username_or_email}")  # Debugging
            
            user = authenticate(request, username=username_or_email, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')  # Redirect to dashboard after login
            else:
                messages.error(request, 'Invalid username/email or password.')
    else:
        form = CustomLoginForm()

    return render(request, 'login.html', {'form': form})

    

from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from .forms import SignUpForm

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])  # Set hashed password
            user.save()
            messages.success(request, "Account created successfully! Please log in.")
            return redirect('login')  # Redirect to login page after signup
    else:
        form = SignUpForm()

    return render(request, 'signup.html', {'form': form})



from .forms import ForgotPasswordForm
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string


def forgotpassword(request):
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)
                profile, created = Profile.objects.get_or_create(user=user)  # Ensure profile exists
                token = get_random_string(50)
                profile.reset_token = token
                profile.save()

                reset_link = request.build_absolute_uri(f'/resetpassword/{token}/')
                send_mail(
                    'Password Reset Request',
                    f'Click the link to reset your password: {reset_link}',
                    'noreply@yourdomain.com',  # Sender email address
                    [email],  # Recipient email address
                    fail_silently=False,
                )

                messages.success(request, "Password reset link has been sent to your email.")
                return redirect('login')  # Redirect to login page after sending reset link
            except User.DoesNotExist:
                messages.error(request, "No user found with this email address.")
    else:
        form = ForgotPasswordForm()

    return render(request, 'forgotpassword.html', {'form': form})



from django.contrib.auth.forms import PasswordResetForm

def resetpassword(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid(): 
            form.save()  
            return redirect('login')  
    else:
        form = PasswordResetForm()
    
    return render(request, 'forgotpassword.html', {'form': form})



from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ChangePasswordForm

@login_required
def changepassword(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST, user=request.user)
        if form.is_valid():
            request.user.set_password(form.cleaned_data['new_password'])
            request.user.save()
            messages.success(request, "Password changed successfully!")
            return redirect('login')
    else:
        form = ChangePasswordForm(user=request.user)

    return render(request, 'changepassword.html', {'form': form})





from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    return render(request, 'dashboard.html', {'username': request.user.username})



from django.db import models
from django.contrib.auth.models import User


@login_required
def profile(request):
    return render(request, 'profile.html', {
        'username': request.user.username,
        'email': request.user.email,
        'date_joined': request.user.date_joined,
        'last_login': request.user.last_login,
    })

from django.contrib.auth.models import User
from .models import Profile

# Example of getting the user's profile and setting a reset token
def generate_reset_token(email):
    try:
        user = User.objects.get(email=email)
        profile = user.profile  # Access the related Profile object
        profile.reset_token = 'random_generated_token'
        profile.save()
        return True
    except User.DoesNotExist:
        return False
