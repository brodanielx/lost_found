from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

GENDER_CHOICES = (
    ('Bro', 'Brother'),
    ('Sis', 'Sister'),
)

class Contact(models.Model):

    STATE_CHOICES = (
        ('FL', 'Florida'),
    )
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    full_name = models.CharField(max_length=254, verbose_name="Name")
    phone_number = models.CharField(max_length=11, unique=True)
    phone_number_formated = models.CharField(max_length=15, verbose_name="Phone #")
    email = models.EmailField(max_length=254)
    gender = models.CharField(max_length=3, choices=GENDER_CHOICES)
    street_address = models.CharField(max_length=254)
    city = models.CharField(max_length=128, default='Tampa')
    state = models.CharField(max_length=2, choices=STATE_CHOICES, default='FL')
    zip_code = models.CharField(max_length=5)
    added_by = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date Added")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Last Updated")

    def save(self, *args, **kwargs):
        self.full_name = '{0} {1}'.format(self.first_name, self.last_name)
        self.phone_number_formated = format_phone_number(self.phone_number)
        super(Contact, self).save(*args, **kwargs)

    def __str__(self):
        return self.full_name

class UserProfile(models.Model):
    POST_CHOICES = (
        ('Coor', 'Study Group Coordinator'),
        ('FOICapt', 'FOI Captain'),
        ('MGTCapt', 'MGT Captain'),
        ('Sect', 'Secretary'),
    )
    user = models.OneToOneField(User)
    gender = models.CharField(max_length=3, choices=GENDER_CHOICES)
    phone_number = models.CharField(max_length=11)
    post = models.CharField(max_length=7, choices=POST_CHOICES)
    def __str__(self):
        return self.user.username

def format_phone_number(phone_number):
    if len(phone_number) == 11:
        phone_number_list = [
            phone_number[0],
            phone_number[1:4],
            phone_number[4:7],
            phone_number[7:]
        ]
        phone_number = '{0[0]}-{0[1]}-{0[2]}-{0[3]}'.format(phone_number_list)
    elif len(phone_number) == 10:
        phone_number_list = [
            phone_number[0:3],
            phone_number[3:6],
            phone_number[6:]
        ]
        phone_number = '{0[0]}-{0[1]}-{0[2]}'.format(phone_number_list)
    elif len(phone_number) == 7:
        phone_number_list = [
            phone_number[0:3],
            phone_number[3:]
        ]
        phone_number = '{0[0]}-{0[1]}'.format(phone_number_list)
    return phone_number
