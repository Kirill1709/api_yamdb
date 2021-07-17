from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = (
        ('user', 'user'),
        ('moderator', 'moderator'),
        ('admin', 'admin')
    )
    email = models.EmailField(unique=True)
    confirmation_code = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        unique=True
    )
    bio = models.TextField(null=True, blank=True, verbose_name="О себе")
    role = models.CharField(
        max_length=20, choices=ROLE_CHOICES, default='User')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
