from datetime import datetime
import os
from django.core.management import BaseCommand
from django.utils import timezone
from openpyxl import Workbook, load_workbook
from homeworkpal_project.settings.base import TEST_DATA_PATH
from project_admin.models import Project

__author__ = 'lberrocal'


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('project_id')

    def handle(self, *args, **options):
        project = Project.objects.get(pk=int(options['project_id']))
        template_filename = os.path.join(TEST_DATA_PATH, '1680_v2.xlsx')
        output_filename = os.path.join(TEST_DATA_PATH, '%s_%s.xlsx' % (project.slug.replace('-','_'), timezone.now().strftime('%Y%m%d_%H%M')))
        wb = load_workbook(template_filename)
        sheet = wb.active
        sheet['D2'] = project.short_name
        sheet['I3'] = datetime.today()
        sheet['A9'] = project.description
        row=20
        for deliverable in project.deliverables.all()[:5]:
            sheet['B%d'%row] = deliverable.name
            sheet['G%d'%row] = deliverable.description
            row += 1
        row=27
        for stakeholder in project.stakeholders.all()[:5]:
            sheet['B%d'%row] = str(stakeholder.employee)
            #sheet['G%d'%row] = deliverable.description
            row += 1

        wb.save(output_filename)
        self.stdout.write('Wrote %s' % output_filename)

