from django.contrib import admin
from .models import TravelAgencyCV, Language, PassportInfo

@admin.register(TravelAgencyCV)
class TravelAgencyCVAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'email', 'created_at', 'updated_at')
    search_fields = ('full_name', 'user__phone_number', 'email')

admin.site.register(Language)
admin.site.register(PassportInfo)