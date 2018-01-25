from django.test import TestCase
from django.contrib.auth.models import User, Group
from contacts.models import Contact
from django.urls import reverse
from django.test import Client

class ContactMethodTests(TestCase):
    def setUp(self):
        u = create_user('user1', 'pass1')
        create_contact('Elijah', 'Muhammad', u)

    def test_save_full_name(self):
        c = Contact.objects.get(pk=1)
        self.assertEqual(
            c.full_name, '{} {}'.format(c.first_name, c.last_name)
        )

    def test_save_phone_number_eleven_digits(self):
        c = Contact.objects.get(pk=1)
        c.phone_number = '18131234567'
        c.save()
        formatted = '1-813-123-4567'
        self.assertEqual(
            c.phone_number_formated, formatted
        )

    def test_save_phone_number_ten_digits(self):
        c = Contact.objects.get(pk=1)
        c.phone_number = '8131234567'
        c.save()
        formatted = '813-123-4567'
        self.assertEqual(
            c.phone_number_formated, formatted
        )

    def test_save_phone_number_seven_digits(self):
        c = Contact.objects.get(pk=1)
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
        create = create_2_contacts_diff_users()
        login = self.client.login(
                username=create['users'][0].username,
                password=create['password']
            )

    def test_user_count(self):
        u = User.objects.get(pk=1)
        count = Contact.objects.filter(added_by=u).count()
        response = self.client.get(reverse('contacts:index'))
        self.assertEqual(
            response.context['contacts_by_user_count'], count
        )

class ContactsShowContactViewTests(TestCase):
    def setUp(self):
        group_name = "View All"
        self.group = Group(name=group_name)
        self.group.save()
        self.create = create_2_contacts_diff_users()
        login = self.client.login(
                username=self.create['users'][0].username,
                password=self.create['password']
            )

    def test_contact_of_diff_user(self):
        c2 = self.create['contacts'][1]
        response = self.client.get(reverse('contacts:show_contact', args=(c2.pk,)))
        self.assertEqual(
            response.status_code, 302
        )

    def test_contact_of_same_user(self):
        c1 = self.create['contacts'][0]
        response = self.client.get(reverse('contacts:show_contact', args=(c1.pk,)))
        self.assertEqual(
            response.status_code, 200
        )

class ContactsEditContactViewTests(TestCase):
    def setUp(self):
        group_name = "View All"
        self.group = Group(name=group_name)
        self.group.save()
        self.create = create_2_contacts_diff_users()
        login = self.client.login(
                username=self.create['users'][0].username,
                password=self.create['password']
            )

    def test_contact_of_diff_user(self):
        c2 = self.create['contacts'][1]
        response = self.client.get(reverse('contacts:edit_contact', args=(c2.pk,)))
        self.assertEqual(
            response.status_code, 302
        )

    def test_contact_of_same_user(self):
        c1 = self.create['contacts'][0]
        response = self.client.get(reverse('contacts:edit_contact', args=(c1.pk,)))
        self.assertEqual(
            response.status_code, 200
        )

class ContactAllContactsViewTests(TestCase):
    def setUp(self):
        group_name = "View All"
        self.group = Group(name=group_name)
        self.group.save()
        self.create = create_2_contacts_diff_users()
        login = self.client.login(
                username=self.create['users'][0].username,
                password=self.create['password']
            )

    def test_user_not_in_group(self):
        response = self.client.get(reverse('contacts:all_contacts'))
        self.assertEqual(
            response.status_code, 302, 'user not in group should not have access'
        )

    def test_user_in_group(self):
        u1 = self.create['users'][0]
        u1.groups.add(self.group)
        u1.save()
        response = self.client.get(reverse('contacts:all_contacts'))
        self.assertEqual(
            response.status_code, 200, 'user in group should have access'
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
    c2 = create_contact('Louis', 'Farrakhan', u2)
    c2.phone_number = '8131234568'
    c2.save()
    return {
        'users': [u1, u2],
        'contacts': [c1, c2],
        'password': 'pass1'
    }
