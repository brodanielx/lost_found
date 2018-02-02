from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.contrib.auth.models import User
from contacts.models import Contact
import os
import logging

logging.basicConfig(filename='test.log', level=logging.DEBUG,
    format='%(asctime)s:%(levelname)s:%(message)s')

class ImportContactsForm(forms.Form):
    helper = FormHelper()
    helper.form_method = 'POST'
    helper.form_class = 'form-horizontal'
    helper.label_class = 'col-5 col-sm-2 text-right pt5'
    helper.field_class = 'col-12 col-sm-10'
    helper.add_input(Submit('submit', 'Submit', css_class='btn-primary'))
    contact_file = forms.FileField(
        label="Contacts: ",
        help_text="'.xlsx' files only"
        )

    def clean_contact_file(self):
        contact_file = self.cleaned_data['contact_file']
        ext = os.path.splitext(contact_file.name)[1]
        try:
            is_file_type(contact_file.name, '.xlsx')
        except Exception as e:
            logging.debug('\n{}'.format(e))
            raise forms.ValidationError('Invalid file. File extension must be \'.xlsx\'.')
        return contact_file

class ContactForm(forms.ModelForm):

    helper = FormHelper()
    helper.form_method = 'POST'
    helper.form_class = 'form-horizontal'
    helper.label_class = 'col-5 col-lg-3 text-right pt5'
    helper.field_class = 'col col-lg-6'
    helper.add_input(Submit('submit', 'Submit', css_class='btn-primary'))

    GENDER_CHOICES = (
        ('Bro', 'Brother'),
        ('Sis', 'Sister'),
    )

    STATE_CHOICES = (
        ('FL', 'Florida'),
    )

    first_name = forms.CharField(
        label="First&nbsp;Name:&nbsp;",
        max_length=128
        )

    last_name = forms.CharField(
        max_length=128,
        label='Last Name: ',
        required=False)

    phone_number = forms.CharField(
        max_length=11,
        label='Phone&nbsp;Number:&nbsp;',
        help_text='Numbers Only'
        )

    email = forms.EmailField(
        max_length=254,
        label='Email Address: ',
        required=False
        )

    gender = forms.ChoiceField(
        label='Gender:&nbsp;',
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

    phone_number_formated = forms.CharField(
        widget=forms.HiddenInput(),
        required=False
        )

    class Meta:
        model = Contact
        exclude = ('added_by', 'created_at', 'updated_at')

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        try:
            is_numbers_only(phone_number)
        except:
            raise forms.ValidationError('Invalid Phone Number: Numbers Only')
        if not (len(phone_number) == 10 or (len(phone_number) == 11 and phone_number[0] == '1')):
            raise forms.ValidationError('Invalid Phone Number')
        return phone_number

    def clean_zip_code(self):
        zip_code = self.cleaned_data['zip_code']
        try:
            is_numbers_only(zip_code)
        except:
            raise forms.ValidationError('Invalid Zip Code: Numbers Only')
        if len(zip_code) > 0 and not len(zip_code) == 5:
            raise forms.ValidationError('Invalid Zip Code: 5 Digits')
        return zip_code

def is_numbers_only(num_string):
    for char in list(num_string):
        int(char)

def is_file_type(filename, ext):
    if os.path.splitext(filename)[1] != ext:
        raise Exception(
            'File Type Error: {0} not {1}'.format(
                os.path.splitext(filename)[1], ext
                )
            )
