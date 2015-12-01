from datetime import date
from django.utils import timezone
import os
from django.core.management import call_command
from io import StringIO
from django.test import TestCase
from homeworkpal_project.settings.base import TEST_OUTPUT_PATH
from maximo.models import MaximoTimeRegister
from maximo.tests.test_excel import TestExcel

__author__ = 'lberrocal'


class TestMaximoCommand(TestCase):
    fixtures = ['employee_fixtures.json', 'maximo_ticket_fixtures.json']

    def test_export_time(self):
        '''
        Verifies the export for MaximoTimeRegister objects to an excel sheet. That contains the following columns:
        Company Id	Username	Date	Hours	Pay Rate	Ticket Type	Ticket Number	Ticket Name	Memo	Project	Project Source
        :return:
        '''
        TestExcel.create_time_registers(date(2015, 9, 1), date(2015, 9, 30))
        out = StringIO()
        filename = os.path.join(TEST_OUTPUT_PATH, '%s_%s.xlsx' % ('test_export_time', timezone.now().strftime('%Y%m%d_%H%M')))
        call_command('maximo_data', filename, export_time=True)
        self.assertTrue(os.path.exists(filename))
        row_data, row_count = TestExcel.get_list_from_workbook(filename, 'Time')
        self.assertEqual(row_count, MaximoTimeRegister.objects.count())
        self.assertEqual(11, len(row_data[0]))
        os.remove(filename)
        self.assertFalse(os.path.exists(filename))

