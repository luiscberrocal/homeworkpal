from django.test import TestCase
from django_auth_ldap.backend import LDAPBackend


class TestLDAP(TestCase):

    def test_get_user(self):
        user = LDAPBackend().populate_user('LBerrocal')
        self.assertIsNotNone(user)
        self.assertEqual('Berrocal Cordoba', user.last_name)
