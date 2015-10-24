import logging
from django.conf import settings
from django.contrib.auth.models import User
from django.test import TestCase
from employee.tests.factories import UserFactory

__author__ = 'luiscberrocal'

logger = logging.getLogger(__name__)

class TestUsers(TestCase):

    def test_create_user(self):
        #settings.configure()
        user = UserFactory.create()
        logger.debug(user)
        self.assertEqual(User.objects.all().count(),1)