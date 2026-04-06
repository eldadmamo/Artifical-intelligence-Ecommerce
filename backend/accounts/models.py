from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
import uuid 

class UserManager(BaseUserManager):
    def create_user(self, email, password = None, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user = self.model(email = email, *extra_fields)
        user.set_password(password)
        user.save(using = self._db)
        return user 
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)
    

class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable= False)
    email = models.EmailField(unique=True, db_index=True)
    phone = models.CharField(max_length=20, blank = True, null = True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    data_joined = models.DataTimeField(default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        db_table = 'users'
        indexes = [
            models.Index(fields=['email'])
        ]

    def __str__(self):
        return self.email
    

class Profile(models.Model):
    GENDER_CHOICES = [
        ('female', 'Female'),
        ('male', 'Male'),
        ('other', 'Other'),
    ]

    SIZE_CHOICES = [
        ('xs', 'Extra Small'),
        ('s', 'Small'),
        ('m', 'Medium'),
        ('l', 'Large'),
        ('xl', 'Extra Large'),
        ('xxl', '2x Large'),
    ]

    SIZE_SYSTEM_CHOICES = [
        ('US', 'US'),
        ('EU', 'EU'),
        ('UK', 'UK'),
    ]

    CURRENCY_CHOICES = [
        ('KSH', 'KSH'),
        ('USD', '$ USD'),
        ('EUR', 'EURO'),
        ('VND', 'VND'),
        ('RUB', 'RUB'),
        ('ETB', 'ETB'),
    ]
    LANGUAGE_CHOICES = [
        ('en', 'English'),
        ('fr', 'France'),
        ('ru', 'PycckNN'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name = 'profile')
    avatar = models.ImageField(upload_to='avatars/', null = True, blank = True)
    name = models.CharField(max_length=100, blank=True, default='')
    gender = models.CharField(max_length=10, choices= GENDER_CHOICES, null = True, blank= True)
    preferred_size = models.CharField(max_length=5, choices=SIZE_CHOICES),
    size_system = models.CharField(max_length=2, choices=SIZE_SYSTEM_CHOICES, default='US')
    language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES, default= 'en')
    currency = models.CharField(max_length=3, choices = CURRENCY_CHOICES, default='KSH')
    country = models.CharField(max_length=100, default='Ethiopia')
    style_preferences = models.JSONField(default=dict, blank= True)
    fcm_token = models.CharField(max_length=255, blank = True, null= True) 
    height_cm = models.DecimalField(max_digits=5, decimal_places=2, null = True, blank = True)
    weight_kg = models.DecimalField(max_digits=5, decimal_places=2, null = True, blank = True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'profiles'

    def __str__(self):
        return f"{self.user.email}'s profile"
    

class Address(models.Model):
    ADDRESS_TYPES = [
        ('home', 'Home'),
        ('work', 'Work'),
        ('other', 'Other')
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable= False)
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name='address')
    address_type = models.CharField(max_length=10, choices= ADDRESS_TYPES, default = 'home')
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    street_address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    district = models.CharField(max_length=100, blank= True)
    country = models.CharField(max_length=100, default='Ethiopia')
    is_default = models.BooleanField(default=False)

    class Meta:
        db_table = 'address'
        verbose_name_plural = 'Addresses'
        indexes = [
            models.Index(fields=['user', 'is_default'])
        ]
    
    def save(self, *args, **kwargs):
        if self.is_default:
            Address.objects.filter(user = self.user, is_default = True).update(
                is_default = True
            )
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.email}'s Address"
