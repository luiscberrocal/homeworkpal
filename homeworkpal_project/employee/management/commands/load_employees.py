from django.contrib.auth.models import User
from django.core.management import BaseCommand
from openpyxl import load_workbook
from employee.models import Employee

__author__ = 'lberrocal'
class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('filename')

    def handle(self, *args, **options):
        self.stdout.write('Filename: %s' % options['filename'])
        wb = load_workbook(filename=options['filename'], data_only=True)
        teachers_sheet = wb['collaborator']
        row_num = 1
        for row in teachers_sheet.rows:
            if row_num > 1:
                values = self._to_list_of_values(row)
                user_dict = self._to_user_dictionary(values)
                user, created = User.objects.get_or_create(username=user_dict['username'], defaults=user_dict)
                if created:
                    self.stdout.write('Created: user %s' % user.username)
                else:
                    for key, value in user_dict.items():
                        setattr(user, key, value)
                    user.save()
                    self.stdout.write('Updated: user %s' % user.username)
                employee_dict = self._to_employee_dict(user, values)
                employee, created = Employee.objects.get_or_create(**employee_dict)
                if created:
                    self.stdout.write('Created: employee %s' % employee)
                else:
                    self.stdout.write('Updated: employee %s' % employee)
                self.stdout.write('-'*70)
                #self.stdout.write(str(values))
            row_num += 1

    def _to_employee_dict(self, user, value_list):
        data = dict()
        data['user'] = user
        data['middle_name'] = value_list[1]
        data['company_id'] = value_list[3]
        data['tenure'] = value_list[9]
        return data

    def _to_user_dictionary(self,value_list):
        data = dict()
        data['username'] = value_list[4]
        data['first_name'] = value_list[0]
        data['last_name'] = value_list[2]
        data['email'] = value_list[5]
        data['password'] = value_list[6]
        return data


    def _to_list_of_values(self, row):
        value_list = []
        for cell in row:
            if cell.value:
                value_list.append(cell.value)
            else:
                value_list.append(None)

        return value_list