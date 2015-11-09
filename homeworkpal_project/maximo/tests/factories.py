import string
from factory import LazyAttribute, Iterator, SubFactory
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyText
from employee.tests.factories import EmployeeFactory
from ..models import MaximoTicket, MaximoTimeRegister
from faker import Factory as FakerFactory
__author__ = 'lberrocal'
faker = FakerFactory.create()

class MaximoTicketFactory(DjangoModelFactory):

    class Meta:
        model = MaximoTicket

    ticket_type = Iterator(MaximoTicket.MAXIMO_TICKET_TYPES, getter=lambda c: c[0])
    number = FuzzyText(length=6, chars=string.digits)
    name = LazyAttribute(lambda x: faker.sentence(nb_words=6, variable_nb_words=True))

class MaximoTimeRegisterFactory(DjangoModelFactory):

    class Meta:
        model = MaximoTimeRegister

    employee = SubFactory(EmployeeFactory)
    ticket = SubFactory(MaximoTicketFactory)
    date = LazyAttribute(lambda x: faker.date_time_between(start_date="-1y", end_date="-1d"))
    regular_hours = 8.0
    description = LazyAttribute(lambda x: faker.sentence(nb_words=6, variable_nb_words=True))