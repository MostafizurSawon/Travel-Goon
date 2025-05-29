from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import User
from .utils import generate_otp, generate_password, send_sms_bdbulksms
from django.contrib import messages
from django.contrib.auth.views import LogoutView
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

import environ
env = environ.Env()
environ.Env.read_env()
# 9774 tjYD6Y77 31012011Sa

BDBULKSMS_TOKEN = env("SMS_TOKEN")


from django.utils import timezone

def guest_register(request):
    if request.user.is_authenticated:
        return redirect('accounts:guest_dashboard')
    if request.method == 'POST':
        phone = request.POST.get('phone_number')
        otp = generate_otp()
        password = generate_password()

        user, created = User.objects.get_or_create(phone_number=phone, defaults={
            'role': 'guest',
            'otp_code': otp,
            'otp_created_at': timezone.now(),
        })

        if not created:
            user.otp_code = otp
            user.otp_created_at = timezone.now()
            user.save(update_fields=['otp_code', 'otp_created_at'])

        user.set_password(password)
        user.save(update_fields=['password'])

        message = f"Your OTP is {otp} and password is {password}"
        status = send_sms_bdbulksms(phone, message, BDBULKSMS_TOKEN)

        if status == "SENT":
            messages.success(request, "OTP sent successfully to your phone.")
            request.session['guest_phone'] = phone
            return redirect('accounts:guest_otp_verify')
        else:
            messages.error(request, "Failed to send OTP SMS. Please try again.")

    return render(request, 'accounts/guest_register.html')

def guest_login(request):
    # If the user is already logged in, redirect to the guest dashboard
    if request.user.is_authenticated:
        return redirect('accounts:guest_dashboard')  

    if request.method == 'POST':
        phone = request.POST.get('phone_number')
        password = request.POST.get('password')

        # Perform the login process as usual
        user = authenticate(request, phone_number=phone, password=password)
        if user is not None and user.role == 'guest':
            login(request, user)
            return redirect('accounts:guest_dashboard')
        else:
            messages.error(request, "Invalid phone number or password.")

    return render(request, 'accounts/guest_login.html')





class LogoutGetAllowedView(LogoutView):
    def get(self, request, *args, **kwargs):
        messages.success(request, "Logged Out Successfully.")
        return self.post(request, *args, **kwargs)



def guest_otp_verify(request):
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        phone = request.session.get('guest_phone')

        if not phone:
            return redirect('accounts:guest_login')

        try:
            user = User.objects.get(phone_number=phone)
        except User.DoesNotExist:
            context = {'error': 'User not found. Please login again.'}
            return render(request, 'accounts/guest_otp_verify.html', context)

        # Optional: Check if OTP expired (e.g., valid for 5 minutes)
        if user.otp_created_at and timezone.now() > user.otp_created_at + timedelta(minutes=5):
            user.otp_code = None
            user.otp_created_at = None
            user.save(update_fields=['otp_code', 'otp_created_at'])
            context = {'error': 'OTP expired. Please request again.'}
            return render(request, 'accounts/guest_otp_verify.html', context)

        if entered_otp == user.otp_code:
            # OTP matched: remove OTP fields
            user.otp_code = None
            user.otp_created_at = None
            user.save(update_fields=['otp_code', 'otp_created_at'])

            # Login user
            login(request, user)

            # Clear phone from session
            request.session.pop('guest_phone', None)

            return redirect('accounts:guest_dashboard')
        else:
            context = {'error': 'Invalid OTP'}
            return render(request, 'accounts/guest_otp_verify.html', context)

    return render(request, 'accounts/guest_otp_verify.html')



@login_required
def guest_dashboard(request):
    if request.user.role != 'guest':
        return redirect('homedemo')  # Prevent non-guests from accessing
    return render(request, 'accounts/guest_dashboard.html')


@login_required
def guest_change_password(request):
    if request.user.role != 'guest':
        return redirect('homedemo')  # Redirect if not guest user

    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Keep user logged in
            messages.success(request, "Your password has been updated successfully.")
            return redirect('accounts:guest_dashboard')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = PasswordChangeForm(user=request.user)

    return render(request, 'accounts/guest_change_password.html', {'form': form})


@login_required
def view_guest_cv(request):
    if request.user.role != 'guest':
        return redirect('homedemo')
    return render(request, 'accounts/guest_cv.html')






# Role Based

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    user_role = request.user.role  # get role from user model
    
    # You can customize the context or templates based on role
    context = {
        'role': user_role,
        'user': request.user,
    }
    
    # Option 1: Use a single template and branch content inside template
    return render(request, 'accounts/dashboard.html', context)
    
    # Option 2 (recommended if very different dashboards):
    # if user_role == 'guest':
    #     return render(request, 'accounts/guest_dashboard.html', context)
    # elif user_role == 'admin':
    #     return render(request, 'accounts/admin_dashboard.html', context)
    # # Add more as needed
