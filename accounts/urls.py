from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('guest-register/', views.guest_register, name='guest_register'),          # OTP + password registration
    path('guest-otp-verify/', views.guest_otp_verify, name='guest_otp_verify'),    # OTP verification
    path('guest-login/', views.guest_login, name='guest_login'),                  # phone+password login
    path('guest-dashboard/', views.guest_dashboard, name='guest_dashboard'),
    path('guest-change-password/', views.guest_change_password, name='guest_change_password'),
    path('guest-cv/', views.view_guest_cv, name='guest_cv'),

]
