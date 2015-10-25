from datetime import datetime
import os
from django.core.management import BaseCommand
from openpyxl import Workbook
from employee.models import CompanyGroup
from homeworkpal_project.settings.base import TEST_DATA_PATH

__author__ = 'luiscberrocal'



class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('group')

    def handle(self, *args, **options):
        group = CompanyGroup.objects.get(name=options['group'])
        filename = os.path.join(TEST_DATA_PATH, '%s_%s.xlsx' % (options['group'], datetime.now().strftime('%Y%m%d_%H%M')))
        wb = Workbook()


        wb.save(filename)



