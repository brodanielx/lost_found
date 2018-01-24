from django.test import TestCase
from django.contrib.auth.models import User
from contacts.models import Contact

class ContactMethodTests(TestCase):
    def test_save_full_name(self):
        c = create_contact()
        self.assertEqual(
            c.full_name, '{} {}'.format(c.first_name, c.last_name)
        )

    def test_save_phone_number_eleven_digits(self):
        c = create_contact()
        c.phone_number = '18131234567'
        c.save()
        formatted = '1-813-123-4567'
        self.assertEqual(
            c.phone_number_formated, formatted
        )

    def test_save_phone_number_ten_digits(self):
        c = create_contact()
        c.phone_number = '8131234567'
        c.save()
        formatted = '813-123-4567'
        self.assertEqual(
            c.phone_number_formated, formatted
        )

    def test_save_phone_number_seven_digits(self):
        c = create_contact()
        c.phone_number = '1234567'
        c.save()
        formatted = '123-4567'
        self.assertEqual(
            c.phone_number_formated, formatted
        )

def create_user():
    u = User(
        username='user1',
        password='password'
    )
    u.save()
    return u

def create_contact():
    u = create_user()
    c = Contact(
        first_name='Elijah',
        last_name='Muhammad',
        added_by=u
    )
    c.save()
    return c
