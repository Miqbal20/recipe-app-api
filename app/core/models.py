from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)

"""Model User"""


class UserManager(BaseUserManager):
    """User Manager"""

    def create_user(self, email, password=None, **extra_fields):
        """Create User"""
        # Check Email
        if not email:
            raise ValueError("User must have an email address")

        # Add User
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None):
        """Create Superuser"""
        return self.create_user(email, password, is_superuser=True, is_staff=True)


class User(AbstractBaseUser, PermissionsMixin):
    """Model User"""

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
