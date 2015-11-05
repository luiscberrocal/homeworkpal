from django.utils import timezone
import os
from django.test import TestCase
from homeworkpal_project.settings.base import TEST_DATA_PATH
from maximo.excel import MaximoExcelData
from maximo.models import MaximoTicket
from maximo.tests.factories import MaximoTicketFactory
import logging

logger = logging.getLogger(__name__)
__author__ = 'lberrocal'


class TestExcel(TestCase):

    def test_load_tickets(self):
        filename = os.path.join(TEST_DATA_PATH, 'maximo_tickets_test_data.xlsx')
        excel_data = MaximoExcelData()
        results = excel_data.load(filename, MaximoExcelData.LOAD_TICKETS)
        self.assertEqual(10, MaximoTicket.objects.count())
        self.assertEqual(10, results['ticket_results']['created'])
        self.assertEqual(0, results['ticket_results']['updated'])
        self.assertEqual(10, results['ticket_results']['rows_parsed'])


    def test_write_tickets(self):
        filename = os.path.join(TEST_DATA_PATH, '%s_%s.xlsx' % ('maximo_tickets', timezone.now().strftime('%Y%m%d_%H%M')))
        excel_data = MaximoExcelData()
        tickets = MaximoTicketFactory.create_batch(10)
        excel_data.save_tickets(filename, tickets)
        self.assertTrue(os.path.exists(filename))
        logger.debug('Wrote: %s' % filename)
        os.remove(filename)
        self.assertFalse(os.path.exists(filename))
