from . import views
from django.urls import path, include

app_name = 'clients'

urlpatterns = [
    path('guest_cv/', views.create_or_update_cv, name='guest_cv'),
]
