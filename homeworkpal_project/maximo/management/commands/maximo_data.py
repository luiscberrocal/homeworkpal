import os

from django.core.management import BaseCommand
from openpyxl import load_workbook
from common.utils import filename_with_datetime, Timer
from homeworkpal_project.settings.base import TEST_OUTPUT_PATH
from maximo.excel import MaximoExcelData, MaximoCSVData
from maximo.models import MaximoTicket, MaximoTimeRegister

__author__ = 'lberrocal'


class Command(BaseCommand):
    '''
    To load Maximo data to the data base use this the --load-time command following these steps:
    1. Create a maximo query using http://127.0.0.1:8000/maximo/sql/. Select the appropiate date ranges. Click on
    copy to clipboard
    2. Open Maximo using Firefox and paste the where clause
    3. Select report TINO-NS-FY16
    4. Export the data to pike separatated data.
    5. Rename the file with the extension .pike
    6. Run
        python manage.py /path/to/data.pike --load-time

    This will have loaded the data to the database. You shoulfd open the log file homeworkpal_project.log for errors


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
            elif extension == '.pike':
                with Timer() as stopwatch:
                    excel_data = MaximoCSVData(stdout=self.stdout, delimiter='|')
                    results = excel_data.load_time_registers(options['filename'])

                self.stdout.write('Parsed: %s' % options['filename'])
                self.stdout.write('Created Registers: %d of %d' % (results['created'], results['rows_parsed']))
                self.stdout.write('Elapsed %s' % stopwatch.elapsed)

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
