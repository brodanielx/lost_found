from django.test import TestCase
from django.contrib.auth.models import User
from contacts.models import Contact

class ContactMethodTests(TestCase):
    def test_save_full_name(self):
        u = User(
            username='user1',
            password='password'
        )
        u.save()
        c = Contact(
            first_name='Elijah',
            last_name='Muhammad',
            added_by=u
        )
        c.save()
        self.assertEqual(
            c.full_name, '{} {}'.format(c.first_name, c.last_name)
        )
