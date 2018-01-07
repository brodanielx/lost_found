import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'lost_found_project.settings')

import django
django.setup()
import logging
from contacts.models import Contact
from django.contrib.auth.models import User
from contacts.forms import is_numbers_only
import openpyxl
import string
import pprint
import json

logging.basicConfig(filename='test.log', level=logging.DEBUG,
    format='%(asctime)s:%(levelname)s:%(message)s')

star_line = '*'*80

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
                'first_name' :
                    handle_none(sheet['{}{}'.format(cols[0], row_str)].value, ''),
                'last_name' :
                    handle_none(sheet['{}{}'.format(cols[1], row_str)].value, ''),
                'gender' :
                    handle_none(sheet['{}{}'.format(cols[3], row_str)].value, ''),
                'email' :
                    handle_none(sheet['{}{}'.format(cols[4], row_str)].value, ''),
                'street_address' :
                    handle_none(sheet['{}{}'.format(cols[5], row_str)].value, ''),
                'city' :
                    handle_none(sheet['{}{}'.format(cols[6], row_str)].value, ''),
                'state' :
                    handle_none(sheet['{}{}'.format(cols[7], row_str)].value, 'FL'),
            }
            try:
                contact['phone_number'] = str(int(handle_none(sheet['{}{}'.format(cols[2], row_str)].value, '')))
            except ValueError:
                contact['phone_number'] = ''

            try:
                contact['zip_code'] = str(int(handle_none(sheet['{}{}'.format(cols[8], row_str)].value, '')))
            except ValueError:
                contact['zip_code'] = ''

            if (validate_contact(contact) and
                phone_number_is_valid(contact['phone_number']) and
                zip_code_is_valid(contact['zip_code']) and
                gender_is_valid(contact['gender'])):
                contacts.append(contact)
            row += 1
        else:
            at_end = True
            logging.debug(
                '{0}{1}{0}Contacts to import: {2} {0}Number of contacts to import: {3}{0}{1}{0}'.format(
                    '\n',
                    star_line,
                    json.dumps(contacts, indent=2),
                    len(contacts)
                )
            )
            return contacts


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
    if len(contacts) > 0:
        user = User.objects.get(username=username)
        for contact in contacts:
            add_contact(contact, user)
        for c in Contact.objects.all():
            print('- {0} - {1} - {2} - {3} - {4}'.format(
                    c.gender, c.full_name, c.phone_number_formated, c.email, c.added_by
                ))

def handle_none(val, rtn):
    if val == None:
        return rtn
    return val

def gender_is_valid(gender):
    gender_title = gender.title()
    if gender_title == 'Bro' or gender_title == 'Sis':
        return True
    return False

def phone_number_is_valid(phone_number_string):
    try:
        is_numbers_only(phone_number_string)
    except ValueError:
        return False
    else:
        if not (len(phone_number_string) == 10
                or (len(phone_number_string) == 11
                and phone_number_string[0] == '1')):
            return False
    return True

def zip_code_is_valid(zip_code_string):
    try:
        is_numbers_only(zip_code_string)
    except ValueError:
        return False
    else:
        if len(zip_code_string) > 0 and not len(zip_code_string) == 5:
            return False
    return True

def validate_contact(contact):
    if (bool(contact['first_name']) and
        bool(contact['phone_number']) and
        bool(contact['gender'])):
        return True
    return False


if __name__ == '__main__':
    contacts = get_contacts_from_excel('mass_upload.xlsx')

    # add_contacts(contacts, 'brodanielx')
