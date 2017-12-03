from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

class Contact(models.Model):
    GENDER_CHOICES = (
        ('Bro', 'Brother'),
        ('Sis', 'Sister'),
    )
    STATE_CHOICES = (
        ('FL', 'Florida'),
    )
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    full_name = models.CharField(max_length=254)
    phone_number = models.CharField(max_length=11, unique=True)
    email = models.EmailField(max_length=254)
    gender = models.CharField(max_length=3, choices=GENDER_CHOICES)
    street_address = models.CharField(max_length=254)
    city = models.CharField(max_length=128, default='Tampa')
    state = models.CharField(max_length=2, choices=STATE_CHOICES, default='FL')
    zip_code = models.CharField(max_length=5)
    added_by = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.full_name = '{0} {1}'.format(self.first_name, self.last_name)
        super(Contact, self).save(*args, **kwargs)

    def __str__(self):
        return self.full_name

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    gender = models.CharField(max_length=6)
    phone_number = models.CharField(max_length=11)
    def __str__(self):
        return self.user.username
