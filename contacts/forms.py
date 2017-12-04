from django import forms
from django.contrib.auth.models import User
from contacts.models import Contact

class ContactForm(forms.ModelForm):
    first_name = forms.CharField(max_length=128, help_text='First Name: ')
    last_name = forms.CharField(max_length=128, help_text='First Name: ')
    phone_number = forms.CharField(max_length=11, help_text='Phone Number: ')
    email = forms.EmailField(max_length=254, help_text='Email Address: ')
    gender = forms.ChoiceField(label='Gender: ', widget=forms.RadioSelect(attrs={'class': 'gender'}), choices=GENDER_CHOICES)
    street_address = forms.CharField(max_length=254, help_text='Street Address: ')
    city = forms.CharField(max_length=128, help_text='City: ')
    state = forms.ChoiceField(lable='State: ', choices=STATE_CHOICES)
    zip_code = forms.CharField(max_length=5)
    full_name = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Contact
        fields = ('')
