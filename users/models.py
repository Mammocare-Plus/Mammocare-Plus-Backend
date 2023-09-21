from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from phonenumber_field.modelfields import PhoneNumberField
from uuid import uuid4
from datetime import datetime
from rest_framework_simplejwt.tokens import RefreshToken

class MCPUserManager(BaseUserManager):
    def create_user(self, username, password, phoneNumber, email=None, **extra_fields):
        if not username:
            raise ValueError("Users must have username")
        if not phoneNumber:
            raise ValueError("Users must have phone number")
        
        user = self.model(
            email = self.normalize_email(email),
            username = username,
            phoneNumber = phoneNumber,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password, phoneNumber, **extra_fields):
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, password, phoneNumber, **extra_fields)

class MCPUser(AbstractBaseUser, PermissionsMixin):

    BLOOD_GROUP_CHOICES = (
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    )

    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Others', 'Others')
    )

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    username = models.CharField(max_length=255, unique=True)
    address = models.CharField(max_length=255, blank=True)
    phoneNumber = PhoneNumberField(unique=True)
    city = models.CharField(max_length=255, blank=True)
    state = models.CharField(max_length=255, blank=True)
    area = models.CharField(max_length=255, blank=True)
    age = models.IntegerField(blank=True, null=True)
    bloodGroup = models.CharField(max_length=3, null=True, blank=True, choices=BLOOD_GROUP_CHOICES)
    gender = models.CharField(max_length=255, choices=GENDER_CHOICES, blank=True)
    aadhar = models.CharField(max_length=255, blank=True)
    profileImage = models.ImageField(upload_to='images/', blank=True, null=True, default='images/default.png')
    isDoctor = models.BooleanField(default=False)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    objects = MCPUserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['phoneNumber']

    def __str__(self):
        return self.username
    
    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return{
            'refresh':str(refresh),
            'access':str(refresh.access_token)
        }
    
    class Meta:
        db_table = 'MCP_user'