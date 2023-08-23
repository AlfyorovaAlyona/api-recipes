"""Database models."""

from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, # contains functiopnality for auth
    BaseUserManager,
    PermissionsMixin, # permissions and fields
)

class UserManager(BaseUserManager):
    """User Manager class."""
    def create_user(self, email, password=None, **extras):
        user = self.model(email=self.normalize_email(email), **extras) # Connected to the user class
        if not email:
            raise ValueError('Email is required!')
        user.set_password(password) # does hashing of the password
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
