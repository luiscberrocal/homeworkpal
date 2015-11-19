from django.core.management import BaseCommand
from common.utils import filename_with_datetime
from homeworkpal_project.settings.base import TEST_OUTPUT_PATH
from project_admin.excel import ProjectAdminExcel
from project_admin.models import ProjectSupport

__author__ = 'LBerrocal'


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('fiscal_year', nargs='?')

    def handle(self, *args, **options):
        excel = ProjectAdminExcel()
        filename = filename_with_datetime(TEST_OUTPUT_PATH, '%s_supports.xlsx' % (options['fiscal_year']))
        supports = ProjectSupport.objects.all()
        excel.export_supports(filename, supports)
        self.stdout.write('Wrote %s' % filename)
