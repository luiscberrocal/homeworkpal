import os

import datetime
from django.test import TestCase

from common.utils import filename_with_datetime
from homeworkpal_project.settings.base import TEST_DATA_PATH, TEST_OUTPUT_PATH
from jira_git.excel import ExcelCommitImporter
import logging

logger = logging.getLogger(__name__)

class TestExcelCommitImporter(TestCase):

    def test_parse_multiple_files(self):
        filenames = [os.path.join(TEST_OUTPUT_PATH, 'Orden_de_Compra', 'navaids_REL340906TINO.pike'),
                     os.path.join(TEST_OUTPUT_PATH, 'Orden_de_Compra', 'ppu_REL340906TINO.pike'),
                     os.path.join(TEST_OUTPUT_PATH, 'Orden_de_Compra', 'signal_REL340906TINO.pike'),
                     os.path.join(TEST_OUTPUT_PATH, 'Orden_de_Compra', 'tas_REL340906TINO.pike')]
        output_filename = filename_with_datetime(TEST_OUTPUT_PATH, 'git_commits.xlsx')
        importer = ExcelCommitImporter()
        commit_count = importer.parse_multiple_files(filenames, output_filename)
        self.assertTrue(os.path.exists(output_filename))
        self.assertEqual(518, commit_count)
        logger.debug('Wrote commits to %s' % output_filename)

    def test_parse_multiple_files_date_filtered(self):
        filenames = [os.path.join(TEST_OUTPUT_PATH, 'Orden_de_Compra', 'navaids_REL340906TINO.pike'),
                     os.path.join(TEST_OUTPUT_PATH, 'Orden_de_Compra', 'ppu_REL340906TINO.pike'),
                     os.path.join(TEST_OUTPUT_PATH, 'Orden_de_Compra', 'signal_REL340906TINO.pike'),
                     os.path.join(TEST_OUTPUT_PATH, 'Orden_de_Compra', 'tas_REL340906TINO.pike')]
        output_filename = filename_with_datetime(TEST_OUTPUT_PATH, 'git_commits_date_filtered.xlsx')
        importer = ExcelCommitImporter()
        commit_count = importer.parse_multiple_files(filenames, output_filename, start_date=datetime.date(2015,10,1), end_date=datetime.date(2016,2,12))
        self.assertTrue(os.path.exists(output_filename))
        self.assertEqual(222, commit_count)
        logger.debug('Wrote commits to %s' % output_filename)
