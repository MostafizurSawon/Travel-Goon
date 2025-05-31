from django.contrib import admin
from .models import SiteSettings, MediaFile

# Register your models here.
admin.site.register(SiteSettings)
admin.site.register(MediaFile)