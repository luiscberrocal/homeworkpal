import string
from django.conf import settings
from django.contrib.auth.models import User
from factory import LazyAttribute, lazy_attribute, SubFactory, Iterator
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyText
from faker import Factory as FakerFactory
from employee.models import TENURE_TYPES, Employee, Position, CompanyGroup, CompanyGroupEmployeeAssignment, \
    PositionAssignment

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

    @classmethod
    def _prepare(cls, create, **kwargs):
        password = kwargs.pop('password', None)
        user = super(UserFactory, cls)._prepare(create, **kwargs)
        if password:
            user.set_password(password)
            if create:
                user.save()
        return user

class EmployeeFactory(DjangoModelFactory):

    class Meta:
        model = Employee
    user = SubFactory(UserFactory)
    middle_name = LazyAttribute(lambda x: faker.first_name())
    company_id = FuzzyText(length=7, chars=string.digits)
    tenure = Iterator(TENURE_TYPES, getter=lambda c: c[0])

class PositionFactory(DjangoModelFactory):

    class Meta:
        model = Position

    number = FuzzyText(length=6, chars=string.digits)
    grade = Iterator(['NM-07', 'NM-09', 'NM-11', 'NM-12', 'NM-13'])
    type = Iterator(TENURE_TYPES, getter=lambda c: c[0])
    owner = None

class CompanyGroupFactory(DjangoModelFactory):

    class Meta:
        model = CompanyGroup

    name = FuzzyText(length=10, chars=string.ascii_uppercase)
    description = 'Company group'

class CompanyGroupEmployeeAssignmentFactory(DjangoModelFactory):

    class Meta:
        model = CompanyGroupEmployeeAssignment

    group = SubFactory(CompanyGroupFactory)
    employee = SubFactory(EmployeeFactory)
    start_date = LazyAttribute(lambda x: faker.date_time_between(start_date="-30y", end_date="-1y"))
    role = CompanyGroupEmployeeAssignment.MEMBER_ROLE

class PositionAssignmentFactory(DjangoModelFactory):

    class Meta:
        model = PositionAssignment

    position = SubFactory(PositionFactory)
    employee = SubFactory(EmployeeFactory)
    start_date = LazyAttribute(lambda x: faker.date_time_between(start_date="-30y", end_date="-1y"))









