from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class User(AbstractUser):
    role = models.ForeignKey(
        "Role",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="users",
    )
    email = models.EmailField(_("email address"), unique=True, max_length=255)
    username = models.CharField(
        max_length=150, blank=True, null=True
    )  # Optional username field
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "username"
    ]  # Fields required when creating a superuser (username is removed)

    def __str__(self):
        return self.email
