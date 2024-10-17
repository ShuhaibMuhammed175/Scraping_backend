from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    """
       Custom manager for the User model providing methods to create regular users and superusers.

       Methods:
       - create_user(email, username, password=None, **extra_fields):
         Creates and returns a regular user with the given email, username, and password.
         Raises:
         - ValueError: If no email is provided.

       - create_superuser(email, username, password=None, **extra_fields):
         Creates and returns a superuser with the given email, username, and password. Superusers
         are provided with additional admin privileges.
       """
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=email,
            username=username,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, username, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model extending AbstractBaseUser and PermissionsMixin for custom authentication.
    """
    email = models.EmailField(
        max_length=255,
        unique=True
    )
    username = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username
