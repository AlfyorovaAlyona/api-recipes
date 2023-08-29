"""Database models."""
from django.conf import settings
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,  # contains functiopnality for auth
    BaseUserManager,
    PermissionsMixin,  # permissions and fields
)


class UserManager(BaseUserManager):
    """User Manager class."""
    def create_user(self, email, password=None, **extras):
        # Connected to the user class
        user = self.model(email=self.normalize_email(email), **extras)
        if not email:
            raise ValueError('Email is required!')
        user.set_password(password)  # does hashing of the password
        user.save(using=self.db)

        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self.db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User class."""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Recipe(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    time_min = models.IntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    link = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.title
