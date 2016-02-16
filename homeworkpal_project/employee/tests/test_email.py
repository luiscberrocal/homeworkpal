from django.core.mail import send_mail
from django.test import TestCase


class TestEmail(TestCase):

    def test_send_email(self):
        send_mail('Test', 'This is a test', 'luis.berrocal.1942@gmail.com', ['lberrocal@pancanal.com'],
                  fail_silently=False)

