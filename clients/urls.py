from . import views
from django.urls import path, include

app_name = 'clients'

urlpatterns = [
    path('guest_cv/', views.create_or_update_cv, name='guest_cv'),
    path('register-passport-info/', views.register_passport_info, name='register_passport_info'),
    path('cv/edit/<int:user_id>/', views.create_or_update_cv, name='edit_cv_by_hr'),  # HR edits guest CV

]

