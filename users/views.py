from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm
from .models import CustomUser  # Import CustomUser model
import uuid  # Import uuid module

# Create your views here.

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # User can't login until email is verified
            user.save()
            user.send_verification_email()
            messages.success(request, 'Your account has been created! Please check your email to verify your account.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def profile(request):
    return render(request, 'users/profile.html')

def verify_email(request, token):
    try:
        user = CustomUser.objects.get(email_verification_token=token)
        if not user.email_verified:
            user.email_verified = True
            user.is_active = True  # Enable the user account
            user.save()
            messages.success(request, 'Your email has been verified successfully. You can now log in.')
            return render(request, 'users/email_verification.html', {'success': True})
        else:
            messages.info(request, 'Your email was already verified.')
            return render(request, 'users/email_verification.html', {'success': True})
    except CustomUser.DoesNotExist:
        messages.error(request, 'Invalid verification link.')
        return render(request, 'users/email_verification.html', {
            'success': False,
            'error_message': 'The verification link is invalid or has expired.'
        })

def resend_verification(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = CustomUser.objects.get(email=email, email_verified=False)
            # Generate new verification token
            user.email_verification_token = uuid.uuid4()
            user.save()
            # Send new verification email
            user.send_verification_email()
            messages.success(request, 'A new verification email has been sent. Please check your inbox.')
        except CustomUser.DoesNotExist:
            messages.error(request, 'No unverified account found with this email address.')
    return redirect('login')
