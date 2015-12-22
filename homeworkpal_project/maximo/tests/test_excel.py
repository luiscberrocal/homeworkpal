from django.utils import timezone
from openpyxl import load_workbook
import os
from django.test import TestCase
from common.utils import filename_with_datetime
from employee.models import Employee
from homeworkpal_project.settings.base import TEST_DATA_PATH, TEST_OUTPUT_PATH
from maximo.excel import MaximoExcelData, parse_hours, MaximoCSVData
from maximo.models import MaximoTicket, MaximoTimeRegister
from maximo.tests.factories import MaximoTicketFactory, MaximoTimeRegisterFactory
import logging
from datetime import date, timedelta

logger = logging.getLogger(__name__)
__author__ = 'lberrocal'


def daterange(start_date, end_date):
    weekend = set([5, 6])
    for n in range(int ((end_date - start_date).days)):
        dt = start_date + timedelta(n)
        if dt.weekday() not in weekend:
            yield dt
        else:
            continue


def get_ticket_position(limit=10):
    count = 0
    a = 0
    while True:
        yield a
        a += 1
        count += 1
        if count == limit:
            a = 0
            count = 0


class TestExcel(TestCase):

    fixtures = ['employee_fixtures.json', 'maximo_ticket_fixtures.json']

    def test_daterange(self):
        start_date = date(2015, 9, 1)
        end_date = date(2015, 9, 30)
        work_days = 0
        for dt in daterange(start_date, end_date):
            work_days +=1
            logger.debug('Date: %s' % dt.strftime('%m-%d %a'))
            #self.assertFalse(dt.weekday() not in set([5, 6]))
        self.assertEqual(21, work_days)

    def test_write_registers(self):
        filename = os.path.join(TEST_OUTPUT_PATH, '%s_%s.xlsx' % ('maximo_time_data', timezone.now().strftime('%Y%m%d_%H%M')))
        excel_data = MaximoExcelData()
        self.create_time_registers(date(2015, 9, 1), date(2015, 9, 30))
        registers = MaximoTimeRegister.objects.all()
        excel_data.save_time_registers(filename, registers)
        self.assertTrue(os.path.exists(filename))
        logger.debug('Wrote: %s' % filename)
        os.remove(filename)
        self.assertFalse(os.path.exists(filename))

    @staticmethod
    def get_list_from_workbook(filename, sheet_name, row_limit=5):
        wb = load_workbook(filename=filename, data_only=True)
        time_sheet = wb[sheet_name]
        row_num = 1
        row_list = list()
        for row in time_sheet.rows:
            if row_num > 1:
                if row_limit < row_num - 1:
                    cell_list = list()
                    for cell in row:
                        cell_list.append(cell.value)
                    row_list.append(cell_list)
            row_num += 1
        return row_list, row_num - 2

    @staticmethod
    def create_time_registers(start_date, end_date):
        tickets = MaximoTicket.objects.all()
        #self.assertEqual(10, len(tickets))
        ticket_pos = get_ticket_position(limit=10)
        employees = Employee.objects.all()
        for dt in daterange(start_date, end_date):
            for employee in employees:
                ticket = tickets[next(ticket_pos)]
                MaximoTimeRegisterFactory.create(employee=employee, date=dt, ticket=ticket)

    def test_export_time_registers(self):
        filename = filename_with_datetime(TEST_OUTPUT_PATH,'maximo_time_data_export.xlsx')
        #os.path.join(TEST_OUTPUT_PATH, '%s_%s.xlsx' % ('maximo_time_data_export', timezone.now().strftime('%Y%m%d_%H%M')))
        excel_data = MaximoExcelData()
        self.create_time_registers(date(2015, 9, 1), date(2015, 9, 30))
        registers = MaximoTimeRegister.objects.all()
        excel_data.export_time_registers(filename, registers)
        self.assertTrue(os.path.exists(filename))
        logger.debug('Wrote: %s' % filename)
        os.remove(filename)
        self.assertFalse(os.path.exists(filename))

    def test_load_tickets(self):
        filename = os.path.join(TEST_DATA_PATH, 'maximo_tickets_test_data.xlsx')
        excel_data = MaximoExcelData()
        results = excel_data.load(filename, MaximoExcelData.LOAD_TICKETS)
        self.assertEqual(20, MaximoTicket.objects.count())
        self.assertEqual(10, results['ticket_results']['created'])
        self.assertEqual(0, results['ticket_results']['updated'])
        self.assertEqual(10, results['ticket_results']['rows_parsed'])
        #MaximoTicket.objects.all().delete()


    def test_write_tickets(self):
        filename = filename_with_datetime(TEST_OUTPUT_PATH,'maximo_tickets.xlsx')
        #os.path.join(TEST_OUTPUT_PATH, '%s_%s.xlsx' % ('maximo_tickets', timezone.now().strftime('%Y%m%d_%H%M')))
        excel_data = MaximoExcelData()
        tickets = MaximoTicketFactory.create_batch(10)
        excel_data.save_tickets(filename, tickets)
        self.assertTrue(os.path.exists(filename))
        row_data, row_count = TestExcel.get_list_from_workbook(filename, excel_data.ticket_sheet)
        self.assertEqual(row_count, 10)
        self.assertEqual(3, len(row_data[0]))
        logger.debug('Wrote: %s' % filename)
        os.remove(filename)
        self.assertFalse(os.path.exists(filename))

    def test_parse_hours(self):
        h = parse_hours('7:30')
        self.assertEqual(h, 7.5)
        h = parse_hours('8:00')
        self.assertEqual(h, 8.0)

    def test_load_time_register(self):
        filename = os.path.join(TEST_DATA_PATH, 'maximo_test_time_data.xlsx')
        excel_data = MaximoExcelData()
        results = excel_data.load(filename, MaximoExcelData.LOAD_TIME)
        self.assertEqual(294, MaximoTimeRegister.objects.count())
        self.assertEqual(294, results['time_results']['created'])
        self.assertEqual(0, results['time_results']['duplicates'])
        self.assertEqual(294, results['time_results']['rows_parsed'])
        self.assertEqual(0, len(results['time_results']['errors']))

    def test_load_time_register_duplicates(self):
        filename = os.path.join(TEST_DATA_PATH, 'maximo_test_time_data.xlsx')
        excel_data = MaximoExcelData()
        excel_data.load(filename, MaximoExcelData.LOAD_TIME)
        results = excel_data.load(filename, MaximoExcelData.LOAD_TIME)
        self.assertEqual(294, MaximoTimeRegister.objects.count())
        self.assertEqual(0, results['time_results']['created'])
        self.assertEqual(294, results['time_results']['duplicates'])
        self.assertEqual(294, results['time_results']['rows_parsed'])
        self.assertEqual(294, len(results['time_results']['errors']))

    def test_load_time_register_duplicates2(self):
        filename = os.path.join(TEST_DATA_PATH, 'maximo_test_time_data2.xlsx')
        excel_data = MaximoExcelData()
        excel_data.load(filename, MaximoExcelData.LOAD_TIME)
        results = excel_data.load(filename, MaximoExcelData.LOAD_TIME)
        self.assertEqual(2, MaximoTimeRegister.objects.count())
        self.assertEqual(0, results['time_results']['created'])
        self.assertEqual(2, results['time_results']['duplicates'])
        self.assertEqual(2, results['time_results']['rows_parsed'])
        self.assertEqual(2, len(results['time_results']['errors']))
        self.assertEqual('Possible duplicate',results['time_results']['errors'][0]['type'] )


class TestMaximoCSVData(TestCase):

    fixtures = ['employee_fixtures.json', 'maximo_ticket_fixtures.json']

    def test_load_time_registers(self):
        filename = os.path.join(TEST_DATA_PATH, 'time_register.csv')
        csv_data = MaximoCSVData()
        results = csv_data.load_time_registers(filename)
        self.assertEqual(59, results['created'])
        self.assertEqual(3, len(results['errors']))

