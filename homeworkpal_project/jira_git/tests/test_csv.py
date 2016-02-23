import os

import datetime
from django.test import TestCase

from homeworkpal_project.settings.base import TEST_DATA_PATH, TEST_OUTPUT_PATH
from jira_git.csv import GitName, GitExportParser
import logging

logger = logging.getLogger(__name__)

class TestGitExportParser(TestCase):

    def test_parse(self):
        filename = os.path.join(TEST_DATA_PATH, 'test_git_export.pike')
        parser = GitExportParser()
        commits = parser.parse(filename)
        self.assertEqual(16, len(commits))
        for commit in commits:
            print(commit)

    def test_parse_date_filtered(self):
        filename = os.path.join(TEST_DATA_PATH, 'test_git_export.pike')
        parser = GitExportParser()
        commits = parser.parse(filename, start_date=datetime.date(2015,11,1), end_date=datetime.date(2015,11,30))
        self.assertEqual(3, len(commits))

    def test_parse_folder_filtered(self):
        folder = os.path.join(TEST_OUTPUT_PATH, 'Orden_de_Compra')
        parser = GitExportParser()
        commits = parser.parse_folder(folder, start_date=datetime.date(2015,11,1), end_date=datetime.date(2015,11,30))
        self.assertEqual(50, len(commits))
        self.assertEqual(8, len(commits[0]))

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

class TestGitName(TestCase):

    def test_get_name(self):
        git_name = GitName()
        name = git_name.get_user('Victor Murillo')
        self.assertEqual('cont-vmurillo', name)

    def test_get_name_wrong_name(self):
        git_name = GitName()
        with self.assertRaises(ValueError):
            name = git_name.get_user('V')


