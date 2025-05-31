from .models import SiteSettings

def site_name(request):
    settings = SiteSettings.objects.first()
    return {'site_name': settings.name if settings else 'Travel Core'}
