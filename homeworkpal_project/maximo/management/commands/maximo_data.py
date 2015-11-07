from django.core.management import BaseCommand
from openpyxl import load_workbook
from maximo.excel import MaximoExcelData
from maximo.models import MaximoTicket

__author__ = 'lberrocal'


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('filename')

    def handle(self, *args, **options):
        excel_data = MaximoExcelData(stdout=self.stdout)
        results = excel_data.load(options['filename'])
        self.stdout.write('Parsed: %s' % options['filename'])
        self.stdout.write('Created Tickets: %d of %d' % (results['ticket_results']['created'], results['ticket_results']['rows_parsed']))
        self.stdout.write('Created Registers: %d of %d' % (results['time_results']['created'], results['time_results']['rows_parsed']))


