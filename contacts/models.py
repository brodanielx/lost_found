from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

class Contact(models.Model):
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    full_name = models.CharField(max_length=128)
    phone_number = models.CharField(max_length=11)
    email = models.EmailField(max_length=254)
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female')
    )
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES)


class Address(models.Model):
    street_address = models.CharField(max_length=254)
    city = models.CharField(max_length=128)
    STATE_CHOICES = (
        ('FL', 'FL'),
    )
    state = models.CharField(max_length=2, choices=STATE_CHOICES, default='FL')
    zipcode = models.CharField(max_length=254)
