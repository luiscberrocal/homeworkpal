import os

import datetime
from django.test import TestCase

from common.utils import filename_with_datetime
from homeworkpal_project.settings.base import TEST_DATA_PATH, TEST_OUTPUT_PATH
from jira_git.cloc import LinesOfCodeCounter
from jira_git.excel import ExcelCommitImporter, ExcelGitReporter, ExcelLineCounterReporter
import logging

from jira_git.git_utils import GitReporter

logger = logging.getLogger(__name__)


class TestExcelLineCounterReporter(TestCase):

    code_folder = r'C:\Users\lberrocal\Documents\codigo_tino_ns'

    def test_write(self):
        folder_name = 'vs_transit_times'
        code_path = os.path.join(self.code_folder, folder_name)
        output_filename = filename_with_datetime(TEST_OUTPUT_PATH, '%s.xlsx' % folder_name)
        cloc = LinesOfCodeCounter(code_path)
        results = cloc.count()
        reporter = ExcelLineCounterReporter()
        reporter.write(output_filename, results)
        self.assertTrue(os.path.exists(output_filename))

    def test_write_multiple(self):
        output_filename = filename_with_datetime(TEST_OUTPUT_PATH, 'tino_ns_lines_of_code.xlsx')
        reporter = ExcelLineCounterReporter()
        for path, sub_folders, files in os.walk(self.code_folder):
            for folder in sub_folders:
                inspection_folder = os.path.join(self.code_folder, folder)
                cloc = LinesOfCodeCounter(inspection_folder)
                results = cloc.count()
                reporter.write(output_filename, results)
            break
        self.assertTrue(os.path.exists(output_filename))


class TestExcelGitReporter(TestCase):

    working_directory = r'C:\Users\lberrocal\Documents\codigo_tino_ns\tino_application_framework_3' #'/Users/luiscberrocal/PycharmProjects/wildbills_project'

    def test_write(self):
        reporter = GitReporter(self.working_directory)
        report = reporter.report()

        excel_reporter = ExcelGitReporter()
        output_filename = filename_with_datetime(TEST_OUTPUT_PATH, 'git_reporter_commits.xlsx')
        commit_count = excel_reporter.write(output_filename, report,start_date=datetime.date(2015,10,1), end_date=datetime.date(2016,2,22))
        self.assertTrue(os.path.exists(output_filename))
        self.assertEqual(len(report['commits']), commit_count)

    def test_write_2(self):
        reporter = GitReporter(self.working_directory)
        report = reporter.report()

        reporter = GitReporter(r'C:\Users\lberrocal\Documents\codigo_tino_ns\vessel_display_web')
        report_2 = reporter.report()

        excel_reporter = ExcelGitReporter()
        output_filename = filename_with_datetime(TEST_OUTPUT_PATH, 'git_reporter_commits.xlsx')
        commit_count = excel_reporter.write(output_filename, report,start_date=datetime.date(2015,10,1), end_date=datetime.date(2016,2,22))
        commit_count_2 = excel_reporter.write(output_filename, report_2, start_date=datetime.date(2015,10,1), end_date=datetime.date(2016,2,22))
        self.assertTrue(os.path.exists(output_filename))
        self.assertEqual(len(report['commits']), commit_count)
        self.assertEqual(len(report_2['commits']), commit_count_2)

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

    def test_parse_multiple_files_single(self):
        filenames = [os.path.join(TEST_DATA_PATH, 'vessel_display_web.txt')]
        importer = ExcelCommitImporter()
        output_filename = filename_with_datetime(TEST_OUTPUT_PATH, 'git_commits_acp_contract.xlsx')
        commit_count = importer.parse_multiple_files(filenames, output_filename, start_date=datetime.date(2015,10,1), end_date=datetime.date(2016,2,12))
        self.assertTrue(os.path.exists(output_filename))
        self.assertEqual(159, commit_count)
        logger.debug('Wrote commits to %s' % output_filename)

    def test_parse_multiple_files_2(self):
        filenames = [os.path.join(TEST_DATA_PATH, 'vessel_display_web.txt'),
                     os.path.join(TEST_DATA_PATH, 'vessel_scheduling_app.txt'),
                     os.path.join(TEST_DATA_PATH, 'vessel_inpections_app.txt'),
                     os.path.join(TEST_DATA_PATH, 'inventory_ppu_app.txt')]
        importer = ExcelCommitImporter()
        output_filename = filename_with_datetime(TEST_OUTPUT_PATH, 'git_commits_acp_contract_02.xlsx')
        commit_count = importer.parse_multiple_files(filenames, output_filename, start_date=datetime.date(2015,10,1), end_date=datetime.date(2016,2,12))
        self.assertTrue(os.path.exists(output_filename))
        self.assertEqual(376, commit_count)
        logger.debug('Wrote commits to %s' % output_filename)


    def test_parse_folder(self):
        folder = os.path.join(TEST_OUTPUT_PATH, 'Orden_de_Compra')
        importer = ExcelCommitImporter()
        output_filename = filename_with_datetime(TEST_OUTPUT_PATH, 'git_commits_parse_folder.xlsx')
        commit_count = importer.parse_folder(folder, output_filename, start_date=datetime.date(2015,10,1), end_date=datetime.date(2016,2,12))
        self.assertTrue(os.path.exists(output_filename))
        self.assertEqual(222, commit_count)
        logger.debug('Wrote commits to %s' % output_filename)

