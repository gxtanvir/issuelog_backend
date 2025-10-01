from django.db import models
import random
import string
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class Company(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Module(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class UserManager(BaseUserManager):
    def create_user(self, user_id, name, email, password=None, **extra_fields):
        if not user_id:
            raise ValueError("User must have a user_id")
        if not email:
            raise ValueError("User must have an email")
        user = self.model(user_id=user_id, name=name, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, user_id, name, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(user_id, name, password, email, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    user_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    companies = models.ManyToManyField(Company, related_name="users")
    modules = models.ManyToManyField(Module, related_name="users")

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "user_id"
    REQUIRED_FIELDS = ["name", "email"]

    def __str__(self):
        return self.user_id
    
class PasswordResetCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        return timezone.now() > self.created_at + timedelta(minutes=10)
    
    @staticmethod
    def generate_code():
        return ''.join(random.choices(string.digits, k = 6))

