from django import forms
from django.contrib.auth.models import User
from contacts.models import Contact

class ContactForm(forms.ModelForm):
    GENDER_CHOICES = (
        ('Bro', 'Brother'),
        ('Sis', 'Sister'),
    )
    STATE_CHOICES = (
        ('FL', 'Florida'),
    )
    first_name = forms.CharField(max_length=128, help_text='First Name: ')
    last_name = forms.CharField(max_length=128, help_text='Last Name: ',
        required=False)
    phone_number = forms.CharField(max_length=11, help_text='Phone Number: ')
    email = forms.EmailField(max_length=254, help_text='Email Address: ',
        required=False)
    gender = forms.ChoiceField(help_text='Gender: ',
        widget=forms.RadioSelect(attrs={'class': 'gender'}), choices=GENDER_CHOICES)
    street_address = forms.CharField(max_length=254, help_text='Street Address: ',
        required=False)
    city = forms.CharField(max_length=128, help_text='City: ',
        required=False)
    state = forms.ChoiceField(help_text='State: ', choices=STATE_CHOICES,
        required=False)
    zip_code = forms.CharField(max_length=5, help_text='Zip Code: ',
        required=False)
    full_name = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Contact
        exclude = ('added_by', 'created_at', 'updated_at')
