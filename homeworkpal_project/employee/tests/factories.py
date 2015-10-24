import string
from django.conf import settings
from django.contrib.auth.models import User
from factory import LazyAttribute, lazy_attribute, SubFactory, Iterator
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyText
from faker import Factory as FakerFactory
from employee.models import TENURE_TYPES, Employee

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

class EmployeeFactory(DjangoModelFactory):

    class Meta:
        model = Employee
    user = SubFactory(UserFactory)
    middle_name = LazyAttribute(lambda x: faker.first_name())
    company_id = FuzzyText(length=7, chars=string.digits)
    tenure = Iterator(TENURE_TYPES, getter=lambda c: c[0])





