
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from accounts.views import LogoutGetAllowedView
from . import views

urlpatterns = [
    path('', views.home, name='home'), 
    path('contact-us/', views.contact, name='contact'),  
    path('packages/', views.packages, name='packages'),  
    path('services/', views.services, name='services'),
    path('about/', views.about, name='about'),  
    path('site-settings/', views.site_settings_view, name='site_settings'),
    path('media-upload/', views.media_upload_view, name='media_upload'), 
]

