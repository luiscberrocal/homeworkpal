import os

import datetime
import shutil

from django.test import TestCase

from common.utils import filename_with_datetime
from homeworkpal_project.settings.base import TEST_DATA_PATH, TEST_OUTPUT_PATH
from ..csv import GitName, GitExportParser
import logging

from jira_git.tests.factories import create_fake_commits_file

logger = logging.getLogger(__name__)

class TestGitExportParser(TestCase):

    clean_output = True

    def test_parse(self):
        filename = filename_with_datetime(TEST_OUTPUT_PATH, 'TestGitExportParser_test_parse.pike')
        create_fake_commits_file(filename, commit_count=25)
        #filename = os.path.join(TEST_DATA_PATH, 'test_git_export.pike')
        parser = GitExportParser()
        commits = parser.parse(filename)
        self.assertEqual(25, len(commits))
        for commit in commits:
            self.assertEqual(9, len(commit))
            self.assertRegex(commit[0], '[a-z0-9]{7}')
            self.assertRegex(commit[1], '^[\w._]{2,}$')
            self.assertRegex(commit[2], '^[\w._]+@[\w.-]+\.[A-Za-z]{2,}$')
            self.assertIsInstance(commit[3], datetime.datetime)
            self.assertIsNotNone(commit[3].tzinfo)
        if self.clean_output:
            os.remove(filename)

    def test_parse_date_filtered(self):
        filename = filename_with_datetime(TEST_OUTPUT_PATH, 'TestGitExportParser_test_parse_date_filtered.pike')
        start_date=datetime.date(2015,10,15)
        end_date=datetime.date(2015,11,30)
        create_fake_commits_file(filename, start_date=start_date, end_date=end_date)

        parser = GitExportParser()
        commits = parser.parse(filename, start_date=datetime.date(2015,11,1), end_date=end_date)
        self.assertEqual(60, len(commits))
        if self.clean_output:
            os.remove(filename)

    def test_parse_folder_filtered(self):
        folder = os.path.join(TEST_OUTPUT_PATH, 'test_parse_folder_filtered')
        if os.path.exists(folder):
            shutil.rmtree(folder)
        os.makedirs(folder)
        date_ranges = [{'base_filename': 'oct.pike',
                        'start_date':datetime.date(2015,10,1),
                        'end_date':datetime.date(2015,10,31)},
                       {'base_filename': 'nov.pike',
                        'start_date':datetime.date(2015,11,1),
                        'end_date':datetime.date(2015,11,30)},
                       {'base_filename': 'dic.pike',
                        'start_date':datetime.date(2015,12,1),
                        'end_date':datetime.date(2015,12,31)},
                       ]
        for date_info in date_ranges:
            filename = filename_with_datetime(folder, date_info['base_filename'])
            create_fake_commits_file(filename,
                                     start_date=date_info['start_date'],
                                     end_date=date_info['end_date'],
                                     commits_per_day=1)
        parser = GitExportParser()

        commits = parser.parse_folder(folder, start_date=datetime.date(2015,11,1),
                                      end_date=datetime.date(2015,11,30))
        self.assertEqual(30, len(commits))

        self.assertEqual(9, len(commits[0]))

    def test_get_project(self):
        parser = GitExportParser()
        desc = 'Adicionar boton para mostrar web page del radar TINO-NS Navigation AidsNAV-13'
        project, issue = parser.get_project(desc)
        self.assertEqual('Navigation Aids', project)

    def test_get_commit_type(self):
        parser = GitExportParser()
        desc = 'Adicionar boton para mostrar web page del radar TINO-NS Navigation AidsNAV-13'
        project = parser.get_commit_type(desc)
        self.assertEqual('COMMIT', project)

        desc = 'Merge branch \'MMMM\' of http://stashy:4444/ms/ns/myproject into MMMM'
        project = parser.get_commit_type(desc)
        self.assertEqual('MERGE', project)

        desc = 'Kits v1.25.3'
        project = parser.get_commit_type(desc)
        self.assertEqual('KITS', project)

        desc = 'Release v10.365.3.4 bal bla'
        project = parser.get_commit_type(desc)
        self.assertEqual('RELEASE', project)

    def test_find_tags(self):
        parser = GitExportParser()
        desc = 'Adicionar boton para mostrar web page del radar TINO-NS Navigation AidsNAV-13'
        tags = parser.find_tags(desc)
        self.assertEqual(tags[0][0], 'NAV')


class TestGitName(TestCase):

    def test_get_name(self):
        git_name = GitName()
        name = git_name.get_user('Victor Murillo')
        self.assertEqual('cont-vmurillo', name)

    def test_get_name_wrong_name(self):
        git_name = GitName()
        with self.assertRaises(ValueError):
            name = git_name.get_user('V')


