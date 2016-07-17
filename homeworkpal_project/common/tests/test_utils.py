import datetime
from unittest import mock
import os

import pytz
from django.test import TestCase
from ..utils import get_fiscal_year, Holiday, Timer, add_date_to_filename
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

    def test_days_in_range_generator(self):
        holiday_manager = Holiday()
        start_date = datetime.date(2016, 1,1)
        end_date = datetime.date(2016,1,31)
        jan_days = list(holiday_manager.days_in_range_generator(start_date, end_date))
        self.assertEqual(31, len(jan_days))
        self.assertEqual(jan_days[0], start_date)
        self.assertEqual(jan_days[30], end_date)

    def test_working_days_for_fiscal_year(self):
        holiday_manager = Holiday()
        months = holiday_manager.working_days_for_fiscal_year(2016)
        self.assertTrue(len(months)==12)
        for month in months:
            logger.debug('%s: %d' % (month['month'], month['working_days']))


class MockPerfCounter(object):

    def __init__(self):
        self.t = 0

    def increment(self, n):
        self.t += n

    def perf_counter(self):
        return self.t


class TestTimer(TestCase):


    def test_get_elapsed_time_str(self):
        clock = MockPerfCounter()
        with mock.patch('time.perf_counter', clock.perf_counter):
            #clock.increment(3600.0)
            stopwatch = Timer()
            stopwatch.start()
            clock.increment(120.5)
            stopwatch.stop()
            self.assertEqual('0 h 2 m 0.50 s', stopwatch.get_elapsed_time_str())

    def test_get_elapsed_time_str_with(self):
        clock = MockPerfCounter()
        with mock.patch('time.perf_counter', clock.perf_counter):
            #clock.increment(3600.0)
            with Timer() as stopwatch:
                clock.increment(360.25)
            self.assertEqual('0 h 6 m 0.25 s', stopwatch.get_elapsed_time_str())


class TestAddDateToFilename(TestCase):

    def setUp(self):
        self.mock_datetime = pytz.timezone('America/Panama').localize(
            datetime.datetime.strptime('2016-07-07 16:40', '%Y-%m-%d %H:%M'))


    @mock.patch('django.utils.timezone.now')
    def test_add_date_to_filename_suffix_path(self, mock_now):
        mock_now.return_value = self.mock_datetime
        filename = r'c:\kilo\poli\namos.txt'
        new_filename = add_date_to_filename(filename)

        self.assertEquals(r'c:\kilo\poli\namos_20160707_1640.txt', new_filename)

        filename = r'c:\kilo\poli\namos.nemo.txt'
        new_filename = add_date_to_filename(filename)

        self.assertEquals(r'c:\kilo\poli\namos.nemo_20160707_1640.txt', new_filename)

        filename = r'/my/linux/path/namos.nemo.txt'
        new_filename = add_date_to_filename(filename)

        self.assertEquals(r'/my/linux/path/namos.nemo_20160707_1640.txt', new_filename)

    @mock.patch('django.utils.timezone.now')
    def test_add_date_to_filename_preffix_path(self, mock_now):
        mock_now.return_value = self.mock_datetime
        filename = r'c:\kilo\poli\namos.txt'
        new_filename = add_date_to_filename(filename, date_position='prefix')
        self.assertEquals(r'c:\kilo\poli\20160707_1640_namos.txt', new_filename)

        filename = r'/my/linux/path/namos.txt'
        new_filename = add_date_to_filename(filename, date_position='prefix')
        self.assertEquals(r'/my/linux/path/20160707_1640_namos.txt', new_filename)


    @mock.patch('django.utils.timezone.now')
    def test_add_date_to_filename_suffix_filename(self, mock_now):
        mock_now.return_value = self.mock_datetime
        filename = r'namos.txt'
        new_filename = add_date_to_filename(filename)
        self.assertEqual('namos_20160707_1640.txt', new_filename)