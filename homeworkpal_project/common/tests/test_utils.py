import datetime
from django.test import TestCase
from ..utils import get_fiscal_year

__author__ = 'lberrocal'

class TestUtils(TestCase):

    def test_get_fiscal_year(self):
        cdates = [[datetime.date(2015, 10, 1), 'AF16'],
                  [datetime.date(2015, 9, 30), 'AF15'],
                  [datetime.date(2016, 1, 5), 'AF16'],]
        for cdate in cdates:
            fy = get_fiscal_year(cdate[0])
            self.assertEqual(cdate[1], fy)

    def test_get_fiscal_year_datetime(self):
        cdates = [[datetime.datetime(2015, 10, 1, 16, 0), 'AF16'],
                  [datetime.datetime(2015, 9, 30, 2, 45), 'AF15'],
                  [datetime.datetime(2016, 1, 5, 3, 45), 'AF16'],]
        for cdate in cdates:
            fy = get_fiscal_year(cdate[0])
            self.assertEqual(cdate[1], fy)