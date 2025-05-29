from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError('Phone number must be provided')
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(phone_number, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    phone_number = models.CharField(max_length=15, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    # Role field: 
    ROLE_CHOICES = (
        ('guest', 'Guest'),
        ('accountant', 'Accountant'),
        ('manager', 'Manager'),
        ('hr', 'HR'),
        ('agent', 'Agent'),
        ('admin', 'Admin'),
        # will add more roles later
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='guest')
    otp_code = models.CharField(max_length=6, blank=True, null=True)  # to store OTP temporarily
    otp_created_at = models.DateTimeField(blank=True, null=True)      # timestamp OTP was created
    
    
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.phone_number
