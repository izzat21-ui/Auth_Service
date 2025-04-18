from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.db.models import CharField, EmailField, ImageField, DateTimeField, BooleanField


class CustomUserManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("The given email must be set")

        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    objects = CustomUserManager()

    AUTH_METHOD_CHOICES = (
        ('admin', 'ADMIN'),
        ('patient', 'PATIENT'),
        ('doctor', 'DOCTOR'),
    )

    username = None

    email = EmailField(blank=True, null=True, unique=True)
    first_name = CharField(max_length=100, blank=True)
    last_name = CharField(max_length=100, blank=True)
    date_joined = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    type_user = CharField(max_length=100, blank=True)
    role = CharField(max_length=50, default='user')
    auth_method = CharField(max_length=10, choices=AUTH_METHOD_CHOICES, default='jwt')
    is_staff = BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
