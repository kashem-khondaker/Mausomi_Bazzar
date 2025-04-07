from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta

class CustomUserManager(BaseUserManager):
    """
    Custom user manager where email is the unique identifier
    for authentication instead of username.
    """
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('Email is required'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    """
    Custom User model where email is the unique identifier
    """
    username = None  # Disable username field
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    is_active = models.BooleanField(_('active'), default=True)
    is_staff = models.BooleanField(_('staff status'), default=False)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    last_login = models.DateTimeField(_('last login'), null=True, blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.email

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip() or self.email

    def get_short_name(self):
        return self.first_name or self.email.split('@')[0]

    def update_last_login(self):
        self.last_login = timezone.now()
        self.save(update_fields=['last_login'])

    @property
    def is_online(self):
        if self.last_login:
            return timezone.now() - self.last_login < timedelta(minutes=5)
        return False

    @property
    def has_complete_profile(self):
        return bool(self.first_name and self.last_name and hasattr(self, 'profile') and self.profile.phone)

class Profile(models.Model):
    """
    User Profile model
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.get_full_name()}'s Profile"

    def clean(self):
        if self.phone and not self.phone.isdigit():
            raise ValidationError({'phone': _('Phone number must contain only digits')})

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
