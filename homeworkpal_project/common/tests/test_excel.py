from django.test import TestCase
from openpyxl import Workbook

from common.excel import ExcelAdapter
from homeworkpal_project.settings.base import TEST_OUTPUT_PATH
from ..utils import filename_with_datetime
from faker import Factory as FakerFactory

faker = FakerFactory.create()

class TestExcelAdapter(TestCase):


    def setUp(self):
        self.filename = filename_with_datetime(TEST_OUTPUT_PATH, 'excel_test_.xlsx')
        wb = Workbook()
        sheet = wb.active
        self.sheet_name ='My New Sheet'
        sheet.title = self.sheet_name
        for row in range(0, 10):
            for column in range(0, 5):
                sheet.cell(column=column+1, row=row+1, value=faker.word())
        wb.save(self.filename)

    def test_convert_to_list(self):
        adapter = ExcelAdapter()
        data = adapter.convert_to_list(self.filename, self.sheet_name)
        self.assertEqual(9, len(data))
        self.assertEqual(5, len(data[0]))