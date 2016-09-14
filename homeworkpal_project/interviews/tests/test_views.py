from django.core.urlresolvers import reverse
from django.test import TestCase
from employee.tests.factories import UserFactory
from interviews.tests.factories import ElegibilityCertificateFactory

__author__ = 'LBerrocal'

class TestInterviewsViews(TestCase):

    def setUp(self):
        # self.client = Client()
        self.username = 'obiwan'
        self.password = 'password'
        self.profile = UserFactory.create(username=self.username,
                                                      password=self.password,
                                                      email='obiwan@jedi.org')

    def test_access(self):
        login = self.client.login(username=self.username,
                                  password=self.password)
        self.assertTrue(login)
        certificate = ElegibilityCertificateFactory.create()
        response = self.client.get(reverse('interviews:certificate-goal', kwargs={'pk': certificate.pk}))
        self.assertEqual(200, response.status_code)