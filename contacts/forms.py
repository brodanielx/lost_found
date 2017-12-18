from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.contrib.auth.models import User
from contacts.models import Contact

class ContactForm(forms.ModelForm):

    helper = FormHelper()
    helper.form_method = 'POST'
    helper.form_class = 'form-horizontal'
    helper.label_class = 'col-lg-4'
    helper.field_class = 'col-lg-8'
    helper.add_input(Submit('Update Contact', 'Update Contact', css_class='btn-primary'))

    GENDER_CHOICES = (
        ('Bro', 'Brother'),
        ('Sis', 'Sister'),
    )

    STATE_CHOICES = (
        ('FL', 'Florida'),
    )

    first_name = forms.CharField(
        label="First Name: ",
        max_length=128
        )

    last_name = forms.CharField(
        max_length=128,
        label='Last Name: ',
        required=False)

    phone_number = forms.CharField(
        max_length=11,
        label='Phone Number: '
        )

    email = forms.EmailField(
        max_length=254,
        label='Email Address: ',
        required=False
        )

    gender = forms.ChoiceField(
        label='Gender: ',
        widget=forms.RadioSelect(attrs={'class': 'gender'}),
        choices=GENDER_CHOICES
        )

    street_address = forms.CharField(
        max_length=254,
        label='Street Address: ',
        required=False
        )

    city = forms.CharField(
        max_length=128,
        label='City: ',
        required=False
        )

    state = forms.ChoiceField(
        label='State: ',
        choices=STATE_CHOICES,
        required=False
        )

    zip_code = forms.CharField(
        max_length=5,
        label='Zip Code: ',
        required=False
        )

    full_name = forms.CharField(
        widget=forms.HiddenInput(),
        required=False
        )

    class Meta:
        model = Contact
        exclude = ('added_by', 'created_at', 'updated_at')
