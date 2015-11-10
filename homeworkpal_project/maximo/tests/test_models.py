from django.test import TestCase
from employee.models import Employee
from maximo.models import MaximoTicket, MaximoTimeRegister
from maximo.tests.factories import MaximoTicketFactory, MaximoTimeRegisterFactory
import logging

__author__ = 'lberrocal'

logger = logging.getLogger(__name__)


class TestMaximoTicket(TestCase):

    def test_create(self):
        ticket = MaximoTicketFactory.create()
        self.assertEqual(6, len(ticket.number))
        self.assertEqual(1, MaximoTicket.objects.count())

    def test_batch_create(self):
        MaximoTicketFactory.create_batch(8, ticket_type='SR')
        MaximoTicketFactory.create_batch(2, ticket_type='WO')
        self.assertEqual(8, MaximoTicket.objects.filter(ticket_type='SR').count())
        self.assertEqual(2, MaximoTicket.objects.filter(ticket_type='WO').count())


class TestMaximoTimeRegister(TestCase):

    fixtures = ['employee_fixtures.json',]

    def test_fixtures_loaded(self):
        self.assertEqual(14, Employee.objects.count())

    def test_create(self):
        register = MaximoTimeRegisterFactory.create()
        self.assertEqual(1, MaximoTimeRegister.objects.count())

    def test_get_employee_total_regular_hours(self):
        register = MaximoTimeRegisterFactory.create()
        register2 = MaximoTimeRegisterFactory.create(employee=register.employee, date=register.date, pay_rate=register.pay_rate)
        registers = MaximoTimeRegister.objects.get_employee_total_regular_hours(employee=register.employee, date=register.date)
        self.assertEqual(2, len(registers))
        self.assertEqual(16, registers['total_regular_hours'])
        self.assertEqual(2, registers['register_count'])
        #self.assertEqual(18, registers[0].total_regular_hours)

    # def test_number_too_long(self):
    #     logger.debug('Method test_number_too_long')
    #     t = MaximoTicketFactory.build(number='ASD')
    #     t.save()
    #     logger.debug('TIcket  %s' % t)


