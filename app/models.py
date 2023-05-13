from django.db import models
from datetime import datetime

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _



class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        # email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, **extra_fields):
        """Create and save a regular User with the given email and password."""
        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """User model."""

    username = None
    email = models.EmailField(_('email address'), unique=True)
    is_active = models.BooleanField(default=True)
    first_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)
    is_staff = models.BooleanField(default=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

class Tag(models.Model):
    title_name = models.CharField(max_length=256)

class Snippet(models.Model):
    text = models.TextField()
    title = models.ForeignKey(Tag,related_name='tag_title', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)
    created_by = models.IntegerField(null=True)



