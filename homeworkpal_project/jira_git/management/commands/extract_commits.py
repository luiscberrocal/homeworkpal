import os

from django.core.management import BaseCommand

from common.utils import filename_with_datetime
from homeworkpal_project.settings.base import TEST_OUTPUT_PATH
from jira_git.git_utils import create_git_excel

__author__ = 'lberrocal'


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('folder')
        parser.add_argument("-o", "--output",
                        dest="filename",
                        help="write report to FILE",
                        metavar="FILE")

    def handle(self, *args, **options):
        last_folder = os.path.split(options['folder'])[1]
        output_filename = filename_with_datetime(TEST_OUTPUT_PATH, '%s_commits.xlsx' % last_folder)
        create_git_excel(options['folder'], output_filename)
        self.stdout.write('Wrote %s' % output_filename)
        