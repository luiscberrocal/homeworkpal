import os

from django.core.management import BaseCommand
from openpyxl import load_workbook
from common.utils import filename_with_datetime
from homeworkpal_project.settings.base import TEST_OUTPUT_PATH
from maximo.excel import MaximoExcelData, MaximoCSVData
from maximo.models import MaximoTicket, MaximoTimeRegister

__author__ = 'lberrocal'


class Command(BaseCommand):
    '''
    python manage.py /path/to/excel.xlsx --load-time
    '''

    def add_arguments(self, parser):
        parser.add_argument('filename', nargs='?')

        parser.add_argument('--load-time',
                            action='store_true',
                            dest='load_time',
                            default=None,
                            help='Load time registers')

        parser.add_argument('--export-time',
                            action='store_true',
                            dest='export_time',
                            default=None,
                            help='Export time registers')

        parser.add_argument('--update-projects',
                            action='store_true',
                            dest='update_projects',
                            default=None,
                            help='Update tickets')

        parser.add_argument('-s', '--start',
                            action='store',
                            dest='start_date',
                            default=None,
                            help='Start Date')

        parser.add_argument('-e', '--end',
                            action='store',
                            dest='end_date',
                            default=None,
                            help='End Date')


    def update_projects(self):
        tickets_with_projects = MaximoTicket.objects.filter(project__isnull=False)
        for ticket in tickets_with_projects:
            orphan_time_registers = MaximoTimeRegister.objects.filter(ticket=ticket, project__isnull=True).update(project=ticket.project)
            self.stdout.write('Updated %d tickets for %s with project %s' % (orphan_time_registers, ticket.name, ticket.project.short_name))

    def handle(self, *args, **options):

        if options['load_time']:
            extension = os.path.splitext(options['filename'])[1]
            if extension == '.xlsx' or extension == '.xls':
                excel_data = MaximoExcelData(stdout=self.stdout)
                results = excel_data.load(options['filename'], action=MaximoExcelData.LOAD_TIME)
                self.stdout.write('Parsed: %s' % options['filename'])
                self.stdout.write('Created Registers: %d of %d' % (results['time_results']['created'], results['time_results']['rows_parsed']))
            elif extension == '.csv':
                excel_data = MaximoCSVData(stdout=self.stdout)
                results = excel_data.load_time_registers(options['filename'])
                self.stdout.write('Parsed: %s' % options['filename'])
                self.stdout.write('Created Registers: %d of %d' % (results['created'], results['rows_parsed']))
        elif options['export_time']:
            excel_data = MaximoExcelData(stdout=self.stdout)
            registers = MaximoTimeRegister.objects.all()
            if options['filename']:
                filename = options['filename']
            else:
                filename = filename_with_datetime(TEST_OUTPUT_PATH, 'Export_Times_%s.xlsx' % ('TINO'))
            excel_data.export_time_registers(filename, registers)
            self.stdout.write('Wrote: %s' % filename)
        elif options['update_projects']:
            self.update_projects()
