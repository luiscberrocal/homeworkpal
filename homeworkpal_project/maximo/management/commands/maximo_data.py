from django.core.management import BaseCommand
from openpyxl import load_workbook
from maximo.excel import MaximoExcelData
from maximo.models import MaximoTicket, MaximoTimeRegister

__author__ = 'lberrocal'


class Command(BaseCommand):
    '''
    python manage.py /path/to/excel.xlsx --load-time
    '''

    def add_arguments(self, parser):
        parser.add_argument('filename')

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

    def handle(self, *args, **options):
        excel_data = MaximoExcelData(stdout=self.stdout)
        if options['load_time']:
            results = excel_data.load(options['filename'], action=MaximoExcelData.LOAD_TIME)
            self.stdout.write('Parsed: %s' % options['filename'])
            # self.stdout.write(
            #     'Created Tickets: %d of %d' % (results['ticket_results']['created'], results['ticket_results']['rows_parsed']))
            self.stdout.write(
                'Created Registers: %d of %d' % (results['time_results']['created'], results['time_results']['rows_parsed']))
        elif options['export_time']:
            registers = MaximoTimeRegister.objects.all()
            excel_data.export_time_registers(options['filename'], registers)
            self.stdout.write('Wrote: %s' % options['filename'])
