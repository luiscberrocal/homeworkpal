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
                user_dict = self._to_user_dictionary(values)
                user, created = User.objects.get_or_create(**user_dict)
                if created:
                    self.stdout.write('Created: user %s' % user.username)
                else:
                    self.stdout.write('Updated: user %s' % user.username)
                #user.save()
                #self.stdout.write(str(values))
            row_num += 1

    def _to_user_dictionary(self,value_list):
        data = dict()
        data['username'] = value_list[0]
        data['first_name'] = value_list[1]
        data['last_name'] = value_list[3]
        data['email'] = value_list[5]
        data['password'] = value_list[7]
        return data


    def _to_list_of_values(self, row):
        value_list = []
        for cell in row:
            if cell.value:
                value_list.append(cell.value)
            else:
                value_list.append(None)

        return value_list

