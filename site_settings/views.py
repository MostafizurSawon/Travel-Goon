from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import SiteSettings
from .forms import SiteSettingsForm, MediaFileUploadForm

def home(request):
    return render(request, 'index.html')

def contact(request):
    return render(request, 'contact-us.html')

def packages(request):
    return render(request, 'package.html')

def services(request):
    return render(request, 'services.html')

def about(request):
    return render(request, 'about-us.html')

@login_required
def site_settings_view(request):
    if request.user.role != 'admin':
        messages.error(request, "You are not authorized to access this page.")
        return redirect('home')

    settings_obj, created = SiteSettings.objects.get_or_create(pk=1)

    if request.method == 'POST':
        form = SiteSettingsForm(request.POST, instance=settings_obj)
        if form.is_valid():
            form.save()
            messages.success(request, "Site settings updated successfully.")
            return redirect('site_settings')
    else:
        form = SiteSettingsForm(instance=settings_obj)

    upload_form = MediaFileUploadForm()

    carousel_fields = [
        {
            'field': form['carousel_image_1'],
            'image_url': settings_obj.carousel_image_1.image.url if settings_obj.carousel_image_1 else None
        },
        {
            'field': form['carousel_image_2'],
            'image_url': settings_obj.carousel_image_2.image.url if settings_obj.carousel_image_2 else None
        },
        {
            'field': form['carousel_image_3'],
            'image_url': settings_obj.carousel_image_3.image.url if settings_obj.carousel_image_3 else None
        }
    ]

    context = {
        'form': form,
        'upload_form': upload_form,
        'carousel_fields': carousel_fields,
    }

    return render(request, 'home/site_settings.html', context)

@login_required
def media_upload_view(request):
    if request.user.role != 'admin':
        messages.error(request, "You are not authorized to upload media.")
        return redirect('home')

    if request.method == 'POST':
        form = MediaFileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Image uploaded successfully.")
            return redirect('site_settings')
    return redirect('site_settings')
