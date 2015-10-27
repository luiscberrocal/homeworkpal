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
        template_filename = os.path.join(TEST_DATA_PATH, '1680.xlsx')
        output_filename = os.path.join(TEST_DATA_PATH, '%s_%s.xlsx' % (project.slug.replace('-','_'), timezone.now().strftime('%Y%m%d_%H%M')))
        wb = load_workbook(template_filename)
        sheet = wb.active
        sheet['D6'] = project.short_name
        wb.save(output_filename)

