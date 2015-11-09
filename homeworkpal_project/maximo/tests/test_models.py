from django.test import TestCase
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


class TestMaximoTimeRegister(TestCase):

    def test_create(self):
        register = MaximoTimeRegisterFactory.create()
        self.assertEqual(1, MaximoTimeRegister.objects.count())

    def test_get_emloyee_total_regular_hours(self):
        register = MaximoTimeRegisterFactory.create()
        register2 = MaximoTimeRegisterFactory.create(employee=register.employee, date=register.date, pay_rate=register.pay_rate)
        registers = MaximoTimeRegister.objects.get_emloyee_total_regular_hours(employee=register.employee, work_date=register.date)
        self.assertEqual(2, len(registers))
        self.assertEqual(16, registers['total_regular_hours'])
        self.assertEqual(2, registers['register_count'])
        #self.assertEqual(18, registers[0].total_regular_hours)

    # def test_number_too_long(self):
    #     logger.debug('Method test_number_too_long')
    #     t = MaximoTicketFactory.build(number='ASD')
    #     t.save()
    #     logger.debug('TIcket  %s' % t)


