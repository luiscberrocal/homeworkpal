import os

import datetime
from django.core.management import BaseCommand

from common.utils import filename_with_datetime
from homeworkpal_project.settings.base import TEST_OUTPUT_PATH
from jira_git.excel import ExcelCommitImporter

__author__ = 'lberrocal'


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('folder')
        parser.add_argument("-o", "--output",
                        dest="filename",
                        help="write report to FILE",
                        metavar="FILE")


    def handle(self, *args, **options):
        self.stdout.write('folder: %s' % options['folder'])
        importer = ExcelCommitImporter()
        output_filename = options.get('filename',
                                      filename_with_datetime(TEST_OUTPUT_PATH, 'git_commits_parse_folder.xlsx'))
        commit_count = importer.parse_folder(options['folder'], output_filename, start_date=datetime.date(2015,10,1), end_date=datetime.date(2016,2,12))
        self.stdout.write('Wrote %d commits to %s' % (commit_count, output_filename))