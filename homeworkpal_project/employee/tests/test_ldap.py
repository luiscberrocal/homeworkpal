from django.test import TestCase
from django_auth_ldap.backend import LDAPBackend


class TestLDAP(TestCase):

    def test_get_user(self):
        user = LDAPBackend().populate_user('OAHerrera')
        self.assertIsNotNone(user)
        self.assertEqual('Herrera Valdes', user.last_name)
