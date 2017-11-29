import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'lost_found_project.settings')

import django
django.setup()
from contacts.models import Contact
from django.contrib.auth.models import User

def populate():

    user = User.objects.get(username='brodanielx')

    first_names = ['Once', 'Was', 'Lost']
    last_names = ['Now', 'Iam', 'Found']
    phone_numbers = ['8131234321', '8139865432', '7277655678']
    email_address = 'bro.danielx@gmail.com'
    genders = ['M', 'F', 'M']

    # for i in range(0, len(phone_numbers)):

    def add_contact(first_name, last_name, phone_number, email_address, gender, user):
        c = Contact.objects.get_or_create(phone_number=phone_number)[0]
        c.first_name = first_name
        c.last_name = last_name
        c.email_address = email_address
        c.gender = gender
        c.user = user
        c.save()



if __name__ == '__main__':
    print('Starting Contacts population script...')
    populate()
