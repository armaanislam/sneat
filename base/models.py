from django.db import models
from django.contrib.auth.models import AbstractUser
from django_countries.fields import CountryField


class User(AbstractUser):
    username = models.CharField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    profile_picture = models.ImageField(null=True)
    email = models.EmailField(unique=True, null=True)
    password = models.CharField(max_length=255)
    address = models.CharField(max_length=255, null=True)
    phone_number = models.CharField(max_length=255, null=True)
    organization = models.CharField(max_length=255, null=True)
    country = CountryField(null=True)
    state = models.CharField(max_length=255, null=True)
    zipcode = models.CharField(max_length=255, null=True)
    LANGUAGE_CHOICES = (
        ("English", "English"),
        ("French", "French"),
        ("German", "German"),
        ("Portugese", "Portugese"),
    )
    language = models.CharField(max_length=9, choices=LANGUAGE_CHOICES, default='English')


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username