from datetime import datetime
import os
from django.core.management import BaseCommand
from openpyxl import Workbook
from openpyxl.styles import Alignment
from employee.models import CompanyGroup
from homeworkpal_project.settings.base import TEST_DATA_PATH
from project_admin.models import ProjectGoal
from django.utils import timezone
__author__ = 'luiscberrocal'


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('group')

    def handle(self, *args, **options):
        group = CompanyGroup.objects.get(name=options['group'])
        filename = os.path.join(TEST_DATA_PATH, '%s_%s.xlsx' % (options['group'], timezone.now().strftime('%Y%m%d_%H%M')))
        wb = Workbook()
        goals = ProjectGoal.objects.filter(project__group__name__exact=options['group']).order_by('employee')
        pos = 1
        current_username = None
        headers = ['No', 'Proyecto', 'Descripción', 'Totalmente Satifactorio', 'Peso']
        for goal in goals:
            if goal.employee.user.username != current_username:
                current_username = goal.employee.user.username
                pos = 1
                sheet = wb.create_sheet(title=current_username)
                sheet['A1'] = 'Nombres: %s  Ip: %s' % (goal.employee, goal.employee.company_id)
                col = 1
                for title in headers:
                    sheet.cell(column=col, row=3, value=title)
                    col += 1
                row = 4
            col = 1
            sheet.cell(column=col, row=row, value=pos)
            col += 1
            cell = sheet.cell(column=col, row=row, value=str(goal.project))
            self._wrap_cell(cell)
            col += 1
            cell = sheet.cell(column=col, row=row, value=str(goal.project.description))
            self._wrap_cell(cell)
            col += 1
            statisfactory = '%f debe estar entregado para el %s' % (goal.expected_advancement,
                                                            goal.project.planned_end_date.strftime('%d-%m-%Y'))
            cell = sheet.cell(column=col, row=row, value=statisfactory)
            self._wrap_cell(cell)
            col += 1
            sheet.cell(column=col, row=row, value=goal.weight)

            row += 1

            self._set_column_widths(sheet)



            print('%d %-50s %s' % (pos, goal.project, goal.employee))
            pos += 1

        wb.save(filename)
        self.stdout.write('Wrote %s'  % filename)

    def _wrap_cell(self, cell):
        alignment=Alignment(horizontal='general',
                            vertical='top',
                            text_rotation=0,
                            wrap_text=True,
                            shrink_to_fit=False,
                            indent=0)
        cell.alignment = alignment

    def _set_column_widths(self, sheet):
        sheet.column_dimensions["A"].width = 5.0
        sheet.column_dimensions["B"].width = 30.0
        sheet.column_dimensions["C"].width = 50.0
        sheet.column_dimensions["D"].width = 15.0
        sheet.column_dimensions["E"].width = 15.0



