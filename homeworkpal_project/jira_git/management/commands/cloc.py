import os

from django.core.management import BaseCommand

from common.utils import filename_with_datetime
from homeworkpal_project.settings.base import TEST_OUTPUT_PATH
from jira_git.cloc import LinesOfCodeCounter
from jira_git.excel import ExcelLineCounterReporter

__author__ = 'lberrocal'


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('folder')
        parser.add_argument("-o", "--output",
                        dest="filename",
                        help="write report to FILE",
                        metavar="FILE")

    def handle(self, *args, **options):
        #last_folder = os.path.split(options['folder'])[1]
        output_filename = filename_with_datetime(TEST_OUTPUT_PATH, 'tino-ns_lines_of_code.xlsx')
        reporter = ExcelLineCounterReporter()
        for path, sub_folders, files in os.walk(options['folder']):
            for folder in sub_folders:
                inspection_folder = os.path.join(options['folder'], folder)
                cloc = LinesOfCodeCounter(inspection_folder)
                results = cloc.count()
                reporter.write(output_filename, results)
                self.stdout.write('%s' % (inspection_folder))
            break
