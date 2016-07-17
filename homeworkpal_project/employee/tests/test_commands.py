import os
import re
from datetime import date
from io import StringIO
from django.core.management import call_command
from django.test import TestCase

from common.utils import filename_with_datetime
from maximo.tests.test_excel import TestExcel


class TestMaximoCommand(TestCase):
    fixtures = ['employee_fixtures.json', 'maximo_ticket_fixtures.json']

    clean_output = True

    def test_export_employees(self):
        TestExcel.create_time_registers(date(2015, 9, 1), date(2015, 9, 30))
        content = StringIO()
        #filename = os.path.join(TEST_OUTPUT_PATH, filename_with_datetime('test_')
        call_command('export_employees', 'TINO-NS', stdout=content)
        content.seek(0)
        lines = content.readlines()
        filename = None
        for line in lines:
            if line.startswith('File export '):
                filename = line.replace('File export ', '').strip()
            regexp = r'^File\sexport\s([\w,\-,\\,:]+)(\.xlsx)'
        self.assertTrue(os.path.exists(filename))
        if self.clean_output:
            os.remove(filename)
            self.assertFalse(os.path.exists(filename))

