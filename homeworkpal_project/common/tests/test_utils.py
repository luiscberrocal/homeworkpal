import datetime
from django.test import TestCase
from ..utils import get_fiscal_year, Holiday
import logging
logger = logging.getLogger(__name__)
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


class TestHolidays(TestCase):

    def test_is_holiday(self):
        holiday = datetime.date(2015,12,25)
        holiday_manager = Holiday()
        self.assertTrue(holiday_manager.is_holiday(holiday))

        non_holiday = datetime.date(2015,12,24)
        self.assertFalse(holiday_manager.is_holiday(non_holiday))

    def test_working_days_between(self):
        holiday_manager = Holiday()
        start_date = datetime.date(2016, 1,1)
        end_date = datetime.date(2016,1,31)
        self.assertEqual(19, holiday_manager.working_days_between(start_date, end_date))
