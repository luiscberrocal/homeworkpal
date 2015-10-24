from django.conf import settings
from django.contrib.auth.models import User
from factory import LazyAttribute, lazy_attribute
from factory.django import DjangoModelFactory
from faker import Factory as FakerFactory
__author__ = 'luiscberrocal'

faker = FakerFactory.create()


class UserFactory(DjangoModelFactory):

    class Meta:
        model = User

    first_name = LazyAttribute(lambda x: faker.first_name())
    last_name = LazyAttribute(lambda x: faker.last_name())
    password = 'user1'

    @lazy_attribute
    def username(self):
        return '%s.%s' % (self.first_name.lower(), self.last_name.lower())

    def email(self):
        return '%s@example.com' % (self.username())
