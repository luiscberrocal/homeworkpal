import os

from django.core.management import call_command
from django.test import TestCase
from io import StringIO

from common.utils import filename_with_datetime
from homeworkpal_project.settings.base import TEST_OUTPUT_PATH


class TestJIRAGitCommand(TestCase):


    def test_convert_commits(self):

        out = StringIO()
        folder = r'C:\Temp\commits' #os.path.join(TEST_OUTPUT_PATH, 'Orden_de_Compra')
        output_filename = filename_with_datetime(TEST_OUTPUT_PATH, 'test_convert_commits.xlsx')
        call_command('convert_commits', folder, filename=output_filename)
        self.assertTrue(os.path.exists(output_filename))

