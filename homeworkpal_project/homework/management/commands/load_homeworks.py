from django.contrib.auth.models import User
from django.core.management import BaseCommand
from openpyxl import load_workbook

__author__ = 'luiscberrocal'

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('filename')

    def handle(self, *args, **options):
        self.stdout.write('Filename: %s' % options['filename'])
        wb = load_workbook(filename = options['filename'], data_only=True)
        teachers_sheet = wb['Teachers']
        row_num = 1
        for row in teachers_sheet.rows:
            if row_num > 1:
                values = self._to_list_of_values(row)
                user = User.objects.create()
                user.username = values[0]
                user.first_name = values[1]
                user.last_name = values[3]
                user.email = values[5]
                user.password = values[7]
                user.save()
                self.stdout.write(str(values))
            row_num += 1

    def _to_list_of_values(self, row):
        value_list = []
        for cell in row:
            if cell.value:
                value_list.append(cell.value)
            else:
                value_list.append(None)

        return value_list

