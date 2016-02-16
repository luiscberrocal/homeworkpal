import os

from django.test import TestCase

from homeworkpal_project.settings.base import TEST_DATA_PATH
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

    def test_get_project(self):
        parser = GitExportParser()
        desc = 'Adicionar boton para mostrar web page del radar TINO-NS Navigation AidsNAV-13'
        project = parser.get_project(desc)
        self.assertEqual('Navigation Aids', project)




class TestGitName(TestCase):

    def test_get_name(self):
        git_name = GitName()
        name = git_name.get_user('Victor Murillo')
        self.assertEqual('cont-vmurillo', name)

    def test_get_name_wrong_name(self):
        git_name = GitName()
        with self.assertRaises(ValueError):
            name = git_name.get_user('V')


