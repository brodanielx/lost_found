import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'lost_found_project.settings')

import django
django.setup()
import logging
from contacts.models import Contact
from django.contrib.auth.models import User
import openpyxl
import string

def get_contacts_from_excel(filename):

    workbook = openpyxl.load_workbook(filename)
    sheet_names = workbook.get_sheet_names()
    sheet = workbook.get_sheet_by_name(sheet_names[0])

    cols = list(string.ascii_uppercase)[1:10]
    row = 9

    at_end = False
    contacts = []

    while not at_end:
        first_cell_of_row = '{}{}'.format(cols[0], str(row))
        if sheet[first_cell_of_row].value != None:
            row_str = str(row)
            contact = {
                'first_name' : sheet['{}{}'.format(cols[0], row_str)].value,
                'last_name' :
                    sheet['{}{}'.format(cols[1], row_str)].value if sheet['{}{}'.format(cols[1], row_str)].value != None else '',
                'phone_number' : str(int(sheet['{}{}'.format(cols[2], row_str)].value)),
                'gender' : sheet['{}{}'.format(cols[3], row_str)].value,
                'email' :
                    sheet['{}{}'.format(cols[4], row_str)].value if sheet['{}{}'.format(cols[4], row_str)].value != None else '',
                'street_address' :
                    sheet['{}{}'.format(cols[5], row_str)].value if sheet['{}{}'.format(cols[5], row_str)].value != None else '',
                'city' :
                    sheet['{}{}'.format(cols[6], row_str)].value if sheet['{}{}'.format(cols[6], row_str)].value != None else '',
                'state' :
                    sheet['{}{}'.format(cols[7], row_str)].value if sheet['{}{}'.format(cols[7], row_str)].value != None else 'FL',
                'zip_code' :
                    str(int(sheet['{}{}'.format(cols[8], row_str)].value)) if sheet['{}{}'.format(cols[8], row_str)].value != None else '',
            }
            if (validateContact(contact)):
                contacts.append(contact)
            row += 1
        else:
            at_end = True
            return contacts


def validateContact(contact):
    if bool(contact['first_name']) and bool(contact['phone_number']) and bool(contact['gender']):
        return True
    return False

def add_contact(contact, user):
    c = Contact.objects.get_or_create(added_by=user, phone_number=contact['phone_number'])[0]
    c.gender = contact['gender']
    c.first_name = contact['first_name']
    c.last_name = contact['last_name']
    c.email = contact['email']
    c.street_address = contact['street_address']
    c.city = contact['city']
    c.state = contact['state']
    c.zip_code = contact['zip_code']
    c.save()

def add_contacts(contacts, username):
    user = User.objects.get(username=username)
    for contact in contacts:
        add_contact(contact, user)
    for c in Contact.objects.all():
        print('- {0} - {1} - {2} - {3} - {4}'.format(
                c.gender, c.full_name, c.phone_number_formated, c.email, c.added_by
            ))

if __name__ == '__main__':
    contacts = get_contacts_from_excel('mass_upload.xlsx')
    add_contacts(contacts, 'brodanielx')
