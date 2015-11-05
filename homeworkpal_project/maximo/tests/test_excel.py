from django.test import TestCase
from maximo.excel import MaximoDataLoader
from maximo.models import MaximoTicket

__author__ = 'lberrocal'


class TestExcel(TestCase):

    def test_load_tickets(self):
        filename = r'/Users/lberrocal/PycharmProjects/homeworkpal/test_data/maximo_data.xlsx'
        loader = MaximoDataLoader()
        results = loader.load(filename, MaximoDataLoader.LOAD_TICKETS)
        self.assertEqual(6, MaximoTicket.objects.count())