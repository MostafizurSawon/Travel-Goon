from django import forms
from .models import SiteSettings, MediaFile

class SiteSettingsForm(forms.ModelForm):
    class Meta:
        model = SiteSettings
        fields = [
            'name', 'title', 'favicon', 'logo',
            'carousel_image_1', 'carousel_image_2', 'carousel_image_3',
            'phone', 'address', 'email',
            'facebook', 'instagram', 'twitter', 'x'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'favicon': forms.Select(attrs={'class': 'form-select select2'}),
            'logo': forms.Select(attrs={'class': 'form-select select2'}),
            'carousel_image_1': forms.Select(attrs={'class': 'form-select select2'}),
            'carousel_image_2': forms.Select(attrs={'class': 'form-select select2'}),
            'carousel_image_3': forms.Select(attrs={'class': 'form-select select2'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'facebook': forms.URLInput(attrs={'class': 'form-control'}),
            'instagram': forms.URLInput(attrs={'class': 'form-control'}),
            'twitter': forms.URLInput(attrs={'class': 'form-control'}),
            'x': forms.URLInput(attrs={'class': 'form-control'}),
        }


class MediaFileUploadForm(forms.ModelForm):
    class Meta:
        model = MediaFile
        fields = ['image']