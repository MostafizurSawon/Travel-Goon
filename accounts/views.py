from django.shortcuts import render, redirect, get_object_or_404
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
from clients.models import PassportInfo, TravelAgencyCV


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
            PassportInfo.objects.get_or_create(user=user)

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
        return redirect('home')  # Prevent non-guests from accessing
    return render(request, 'accounts/guest_dashboard.html')


@login_required
def guest_change_password(request):
    if request.user.role != 'guest':
        return redirect('home')  # Redirect if not guest user

    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Keep user logged in
            messages.success(request, "Your password has been updated successfully.")
            return redirect('accounts:dashboard')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = PasswordChangeForm(user=request.user)

    return render(request, 'accounts/guest_change_password.html', {'form': form})


@login_required
def view_guest_cv(request):
    if request.user.role != 'guest':
        return redirect('home')
    return render(request, 'accounts/guest_cv.html')






# Role Based

def role_based_login(request):
    # Redirect if already logged in
    if request.user.is_authenticated:
        if request.user.role == 'hr':
            return redirect('accounts:hr_dashboard')
        elif request.user.role == 'admin':
            return redirect('accounts:admin_dashboard')
        else:
            return redirect('accounts:guest_dashboard')  

    if request.method == 'POST':
        phone = request.POST.get('phone_number')
        password = request.POST.get('password')

        user = authenticate(request, phone_number=phone, password=password)

        # Allow all except guests here
        if user is not None and user.role != 'guest':
            login(request, user)
            print(user.role)
            if request.user.role == 'hr':
                return redirect('accounts:hr_dashboard')
            elif request.user.role == 'admin':
                return redirect('accounts:admin_dashboard')
        else:
            messages.error(request, "Invalid phone number or password for this login.")

    return render(request, 'accounts/role_based_login.html')

@login_required
def admin_dashboard(request):
    if request.user.role == 'admin':
        return render(request, 'accounts/admin_dashboard.html')
    return redirect('home')



    
@login_required
def hr_dashboard(request):
    if request.user.role != 'hr':
        return redirect('home')
    
    
    # HR dashboard logic here
    return render(request, 'accounts/hr_dashboard.html')




@login_required
def hr_view_guests_passport(request):
    # Ensure only HR users can access
    if request.user.role != 'hr':
        return redirect('home')  # or permission denied page

    # Get all PassportInfo for users with role 'guest'
    guest_passports = PassportInfo.objects.filter(user__role='guest')

    context = {
        'guest_passports': guest_passports,
    }
    return render(request, 'hr/hr_guest_passports.html', context)


@login_required
def hr_guest_cvs_list(request):
    if request.user.role != 'hr':
        return redirect('home')  # or permission denied page
    guest_cvs = TravelAgencyCV.objects.select_related('user').all()
    return render(request, 'hr/hr_guest_cvs_list.html', {'guest_cvs': guest_cvs})




@login_required
def guest_cv_detail(request, pk):
    if request.user.role != 'hr':
        return redirect('home')  
    cv = TravelAgencyCV.objects.get(pk=pk)
    return render(request, 'hr/guest_cv_detail.html', {'cv': cv})



# from clients.forms import TravelAgencyCVForm

# @login_required
# def guest_cv_detail(request, pk):
#     if request.user.role != 'hr':
#         return redirect('home')

#     cv = get_object_or_404(TravelAgencyCV, pk=pk)

#     # Optional: confirm this cv belongs to a guest
#     if cv.user.role != 'guest':
#         return redirect('home')

#     if request.method == 'POST':
#         form = TravelAgencyCVForm(request.POST, request.FILES, instance=cv)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'CV updated successfully.')
#             return redirect('accounts:guest_cv_detail', pk=cv.pk)  # Or wherever you want to redirect
#         else:
#             messages.error(request, 'Please correct the errors below.')
#     else:
#         form = TravelAgencyCVForm(instance=cv)

#     return render(request, 'hr/guest_cv_edit.html', {'form': form, 'cv': cv})
