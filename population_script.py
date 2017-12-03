import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'lost_found_project.settings')

import django
django.setup()
from contacts.models import Contact
from django.contrib.auth.models import User

def populate():

    user = User.objects.get(username='brodanielx')
    email = 'bro.danielx@gmail.com'
    city = 'Tampa'
    state = 'FL'

    first_names = ['Once', 'Was', 'Lost']
    last_names = ['Now', 'Iam', 'Found']
    phone_numbers = ['8131234321', '8139865432', '7277655678']
    genders = ['Bro', 'Sis', 'Bro']

    for i in range(0, len(phone_numbers)):
        add_contact(first_names[i], last_names[i], phone_numbers[i], email ,genders[i], state, user)

    for c in Contact.objects.all():
        print('- {0} - {1} - {2}'.format(c.gender, c.full_name, c.phone_number))

def add_contact(first_name, last_name, phone_number, email, gender, state, user):
    c = Contact.objects.get_or_create(added_by=user, phone_number=phone_number)[0]
    c.first_name = first_name
    c.last_name = last_name
    c.email = email
    c.gender = gender
    c.save()


if __name__ == '__main__':
    print('\nStarting Contacts population script...\n')
    populate()
    print('\n')
