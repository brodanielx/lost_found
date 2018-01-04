import os
import openpyxl
import string


def validateContact(contact):
    if bool(contact['first_name']) and bool(contact['phone_number']) and bool(contact['gender']):
        return True
    return False

workbook = openpyxl.load_workbook('mass_upload.xlsx')
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
            'phone_number' : sheet['{}{}'.format(cols[2], row_str)].value,
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
                sheet['{}{}'.format(cols[8], row_str)].value if sheet['{}{}'.format(cols[8], row_str)].value != None else '',
        }
        if (validateContact(contact)):
            contacts.append(contact)
        row += 1
    else:
        at_end = True

for contact in contacts:
    print(' {gender} - {first_name} {last_name} - {phone_number} - {email} - {street_address} - {city} - {state} - {zip_code} '.format(**contact))
