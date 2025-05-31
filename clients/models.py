from django.db import models
from django.conf import settings

class Language(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class TravelAgencyCV(models.Model):
    BLOOD_GROUP_CHOICES = [
        ('A+', 'A+'), ('A-', 'A-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('O+', 'O+'), ('O-', 'O-'),
        ('Other', 'Other'),
    ]

    LANGUAGE_CHOICES = [
        ('English', 'English'),
        ('Bangla', 'Bangla'),
        ('Other', 'Other'),
    ]

    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]

    MARRIED_CHOICES = [
        ('Yes', 'Yes'),
        ('No', 'No'),
    ]

    EDUCATION_CHOICES = [
        ('SSC', 'SSC'),
        ('HSC', 'HSC'),
        ('HONOURS', 'Honours'),
        ('Others', 'Others'),
    ]

    JOB_STATUS_CHOICES = [
        ('Unemployed', 'Unemployed'),
        ('Employed', 'Employed'),
        ('Student', 'Student'),
        ('Others', 'Others'),
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cv')

    # Names
    full_name = models.CharField("Full Name (English)", max_length=200)
    full_name_bn = models.CharField("Full Name (Bangla)", max_length=200, blank=True)

    bio = models.TextField(blank=True, help_text="A brief introduction about yourself")


    # Blood Group
    blood_group = models.CharField(max_length=10, choices=BLOOD_GROUP_CHOICES, default='Other')
    blood_group_other = models.CharField(max_length=20, blank=True, help_text="If Other, specify here")

    # Photo
    profile_picture = models.ImageField(upload_to='cv_pictures/', null=True, blank=True)

    # Language
    languages = models.ManyToManyField(Language, blank=True, related_name='cvs')
    language_other = models.CharField(max_length=255, blank=True, help_text="If Other, specify additional languages here")


    # Contact & Personal info
    email = models.EmailField()
    date_of_birth = models.DateField()
    nationality = models.CharField(max_length=100)
    national_id = models.IntegerField(unique=True, help_text="National ID", blank=True, null=True)

    # Addresses
    current_address = models.TextField()
    is_permanent_same_as_current = models.BooleanField(default=False)
    permanent_address = models.TextField(blank=True)

    # Family info
    fathers_name = models.CharField(max_length=200)
    fathers_mobile = models.CharField(max_length=20)
    fathers_nid = models.CharField(max_length=20)

    mothers_name = models.CharField(max_length=200)
    mothers_mobile = models.CharField(max_length=20)
    mothers_nid = models.CharField(max_length=20)

    # Other personal info
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='Male')
    married = models.CharField(max_length=5, choices=MARRIED_CHOICES, default='No')

    # Education
    last_education = models.CharField(max_length=20, choices=EDUCATION_CHOICES, default='SSC')
    last_education_other = models.CharField(max_length=100, blank=True, help_text="If Others, specify here")
    last_education_result = models.CharField(max_length=100)
    last_education_passing_year = models.PositiveIntegerField()

    # Job info
    current_job_status = models.CharField(max_length=20, choices=JOB_STATUS_CHOICES, default='Unemployed')
    current_job_status_other = models.CharField(max_length=100, blank=True, help_text="If Others, specify here")
    current_job_title = models.CharField(max_length=200, blank=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # If permanent address same as current, copy it
        if self.is_permanent_same_as_current:
            self.permanent_address = self.current_address
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.full_name}'s CV"





class PassportInfo(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='passport_info')
    
    passport_number = models.CharField(max_length=20)
    full_name = models.CharField(max_length=200)
    date_of_birth = models.DateField()
    place_of_birth = models.CharField(max_length=100)
    nationality = models.CharField(max_length=100, default='Bangladeshi')
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])
    father_name = models.CharField(max_length=200)
    mother_name = models.CharField(max_length=200)
    spouse_name = models.CharField(max_length=200, blank=True, null=True)
    issue_date = models.DateField()
    expiry_date = models.DateField()
    place_of_issue = models.CharField(max_length=100)
    passport_photo = models.ImageField(upload_to='passport_photos/', null=True, blank=True)
    signature = models.ImageField(upload_to='signatures/', null=True, blank=True)

    def __str__(self):
        return f"{self.user.phone_number}'s Passport Info"
