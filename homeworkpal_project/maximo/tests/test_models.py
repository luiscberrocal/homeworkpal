from django.test import TestCase
from maximo.models import MaximoTicket
from maximo.tests.factories import MaximoTicketFactory
import logging

__author__ = 'lberrocal'

logger = logging.getLogger(__name__)

class TestMaximoTicket(TestCase):

    def test_create(self):
        ticket = MaximoTicketFactory.create()
        self.assertEqual(6, len(ticket.number))
        self.assertEqual(1, MaximoTicket.objects.count())

    # def test_number_too_long(self):
    #     logger.debug('Method test_number_too_long')
    #     t = MaximoTicketFactory.build(number='ASD')
    #     t.save()
    #     logger.debug('TIcket  %s' % t)


