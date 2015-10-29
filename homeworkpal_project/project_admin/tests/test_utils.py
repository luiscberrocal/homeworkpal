from datetime import date
import logging
from django.test import TestCase
from project_admin.utils import Holiday

__author__ = 'LBerrocal'

logger = logging.getLogger(__name__)
class TestHolidays(TestCase):

    def test_is_holiday(self):
        holiday = date(2015,12,25)
        holiday_manager = Holiday()
        self.assertTrue(holiday_manager.is_holiday(holiday))

        non_holiday = date(2015,12,24)
        self.assertFalse(holiday_manager.is_holiday(non_holiday))
