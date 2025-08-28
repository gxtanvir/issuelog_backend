from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

class UserManager(BaseUserManager):
    use_in_migrations = True

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

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(user_id, name, password, **extra_fields)


class User(AbstractUser):
    username = None  # remove default username field
    user_id = models.CharField(max_length=6, unique=True)
    name = models.CharField(max_length=100)

    # ✅ NEW FIELDS
    companies = models.JSONField(default=list, blank=True)  
    modules = models.JSONField(default=list, blank=True)    

    USERNAME_FIELD = "user_id"
    REQUIRED_FIELDS = ["name"]

    objects = UserManager()

    def __str__(self):
        return self.user_id
