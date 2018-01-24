from django.test import TestCase
from django.contrib.auth.models import User, Group
from contacts.models import Contact
from django.urls import reverse
from django.test import Client

class ContactMethodTests(TestCase):
    def test_save_full_name(self):
        u = create_user('user1', 'pass1')
        c = create_contact('Elijah', 'Muhammad', u)
        self.assertEqual(
            c.full_name, '{} {}'.format(c.first_name, c.last_name)
        )

    def test_save_phone_number_eleven_digits(self):
        u = create_user('user1', 'pass1')
        c = create_contact('Elijah', 'Muhammad', u)
        c.phone_number = '18131234567'
        c.save()
        formatted = '1-813-123-4567'
        self.assertEqual(
            c.phone_number_formated, formatted
        )

    def test_save_phone_number_ten_digits(self):
        u = create_user('user1', 'pass1')
        c = create_contact('Elijah', 'Muhammad', u)
        c.phone_number = '8131234567'
        c.save()
        formatted = '813-123-4567'
        self.assertEqual(
            c.phone_number_formated, formatted
        )

    def test_save_phone_number_seven_digits(self):
        u = create_user('user1', 'pass1')
        c = create_contact('Elijah', 'Muhammad', u)
        c.phone_number = '1234567'
        c.save()
        formatted = '123-4567'
        self.assertEqual(
            c.phone_number_formated, formatted
        )

class ContactsIndexViewTests(TestCase):
    def setUp(self):
        group_name = "View All"
        self.group = Group(name=group_name)
        self.group.save()

    def test_user_count(self):
        create = create_2_contacts_diff_users()
        login = self.client.login(
                username=create['users'][0].username,
                password=create['password']
            )
        response = self.client.get(reverse('contacts:index'))
        print(response)
        self.assertEqual(
            1, 1
        )



def create_user(uname, pword):
    u = User(
        username=uname,
    )
    u.set_password(pword)
    u.save()
    return u

def create_contact(first, last, user):
    c = Contact(
        first_name=first,
        last_name=last,
        added_by=user
    )
    c.save()
    return c

def create_2_contacts_diff_users():
    u1 = create_user('user1', 'pass1')
    u2 = create_user('user2', 'pass2')
    c1 = create_contact('Elijah', 'Muhammad', u1)
    c1.phone_number = '8131234567'
    c1.save()
    c2 = create_contact('Louis', 'Farrakhan', u1)
    c2.phone_number = '8131234568'
    c2.save()
    return {
        'users': [u1, u2],
        'contacts': [c1, c2],
        'password': 'pass1'
    }
