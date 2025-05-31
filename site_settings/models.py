from django.db import models

class MediaFile(models.Model):
    image = models.ImageField(upload_to='media_library/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.image.name or f"MediaFile {self.pk}"

    def image_tag(self):
        if self.image:
            return format_html('<img src="{}" style="height: 100px;" />', self.image.url)
        return ""
    image_tag.short_description = 'Preview'


class SiteSettings(models.Model):
    # General Site Info
    name = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    favicon = models.ForeignKey(MediaFile, on_delete=models.SET_NULL, blank=True, null=True, related_name='favicon')
    logo = models.ForeignKey(MediaFile, on_delete=models.SET_NULL, blank=True, null=True, related_name='logo')

    # Carousel Images
    carousel_image_1 = models.ForeignKey(MediaFile, on_delete=models.SET_NULL, blank=True, null=True, related_name='carousel_1')
    carousel_image_2 = models.ForeignKey(MediaFile, on_delete=models.SET_NULL, blank=True, null=True, related_name='carousel_2')
    carousel_image_3 = models.ForeignKey(MediaFile, on_delete=models.SET_NULL, blank=True, null=True, related_name='carousel_3')

    # Contact Info
    phone = models.CharField(max_length=50, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    # Social Links
    facebook = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    x = models.URLField(blank=True, null=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name or f"SiteSettings {self.pk}"
