from datetime import datetime
import os
from django.core.management import BaseCommand
from openpyxl import Workbook
from employee.models import CompanyGroup
from homeworkpal_project.settings.base import TEST_DATA_PATH
from project_admin.models import ProjectGoal

__author__ = 'luiscberrocal'


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('group')

    def handle(self, *args, **options):
        group = CompanyGroup.objects.get(name=options['group'])
        filename = os.path.join(TEST_DATA_PATH, '%s_%s.xlsx' % (options['group'], datetime.now().strftime('%Y%m%d_%H%M')))
        wb = Workbook()
        goals = ProjectGoal.objects.filter(project__group__name__exact=options['group']).order_by('employee')
        pos = 1
        current_username = None
        for goal in goals:
            if goal.employee.user.username != current_username:
                current_username = goal.employee.user.username
                pos = 1
            print('%d %-50s %s' % (pos, goal.project, goal.employee))
            pos += 1

        wb.save(filename)
        self.stdout.write('Wrote %s'  % filename)



