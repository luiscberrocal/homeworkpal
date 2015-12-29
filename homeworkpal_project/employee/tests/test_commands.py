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

    def test_export_employees(self):
        TestExcel.create_time_registers(date(2015, 9, 1), date(2015, 9, 30))
        content = StringIO()
        #filename = os.path.join(TEST_OUTPUT_PATH, filename_with_datetime('test_')
        call_command('export_employees', 'TINO-NS', stdout=content)
        content.seek(0)
        lines = content.readlines()
        filename = None
        for line in lines:
            regexp = r'^File\sexport\s([\w,\-,\\,:]+)(\.xlsx)'
            pattern  = re.compile(regexp)
            match = pattern.match(line)
            if match:
                filename =  match.group(1) + match.group(2)
                #print(filename)
            #print(line)
        self.assertTrue(os.path.exists(filename))
