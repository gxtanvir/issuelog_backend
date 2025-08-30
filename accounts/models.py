from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, user_id, name, password=None, **extra_fields):
        if not user_id:
            raise ValueError("The User ID must be set")
        user = self.model(user_id=user_id, name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, user_id, name, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(user_id, name, password, **extra_fields)


class User(AbstractUser):
    username = None  # remove default username
    user_id = models.CharField(max_length=15, unique=True)
    name = models.CharField(max_length=150)
    companies = models.JSONField(default=list, blank=True)
    modules = models.JSONField(default=list, blank=True)

    USERNAME_FIELD = "user_id"   # 👈 login field
    REQUIRED_FIELDS = ["name"]

    objects = UserManager()

    def __str__(self):
        return self.user_id
