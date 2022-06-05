from django.db import models
from django.contrib.auth.models import AbstractUser
from django_countries.fields import CountryField


class User(AbstractUser):
    username = models.CharField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(null=True)
    password = models.CharField(max_length=255)
    address = models.CharField(max_length=255, null=True)
    phone_number = models.CharField(max_length=255, null=True)
    organization = models.CharField(max_length=255, null=True)
    country = CountryField(null=True)
    state = models.CharField(max_length=255, null=True)
    zipcode = models.CharField(max_length=255, null=True)
    LANGUAGES = (
        ("English", "English"),
        ("German", "German"),
        ("French", "French"),
        ("Portugese", "Portugese"),
    )
    language = models.CharField(max_length=20, blank=True, default='', choices=LANGUAGES, verbose_name="Languages")
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at', '-updated_at']

    def __str__(self):
        return self.username

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
