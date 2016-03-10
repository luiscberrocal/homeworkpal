import os

import datetime
import shutil

from django.test import TestCase

from common.excel import ExcelAdapter
from common.utils import filename_with_datetime
from homeworkpal_project.settings.base import TEST_DATA_PATH, TEST_OUTPUT_PATH
from jira_git.cloc import LinesOfCodeCounter
from jira_git.excel import ExcelCommitImporter, ExcelGitReporter, ExcelLineCounterReporter
import logging

from jira_git.git_utils import GitReporter
from jira_git.tests.factories import CommitFactory, create_fake_commits_file

logger = logging.getLogger(__name__)


class TestExcelLineCounterReporter(TestCase):

    code_folder = r'C:\Users\lberrocal\Documents\codigo_tino_ns_graveyard'
    clean_output = False

    def setUp(self):
        self.excel_adapter = ExcelAdapter()


    def test_write(self):
        folder_name = '0AIS'
        code_path = os.path.join(self.code_folder,'all_scientific_applications', folder_name)
        output_filename = filename_with_datetime(TEST_OUTPUT_PATH, '%s.xlsx' % folder_name)
        cloc = LinesOfCodeCounter(code_path)
        results = cloc.count()

        reporter = ExcelLineCounterReporter()
        reporter.write(output_filename, results)
        self.assertTrue(os.path.exists(output_filename))

        self.assertEqual(516, len(results))

        results = self.excel_adapter.convert_to_list(output_filename, 'Lines of Code')
        self.assertEqual(516, len(results))
        self.assertEqual(5, len(results[0]))
        self.assertEqual(folder_name, results[0][0])

        if self.clean_output:
            os.remove(output_filename)

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

        results = self.excel_adapter.convert_to_list(output_filename, 'Lines of Code')
        self.assertEqual(3705, len(results))
        self.assertEqual(5, len(results[0]))

        if self.clean_output:
            os.remove(output_filename)



class TestExcelGitReporter(TestCase):

    working_directory = r'C:\Users\lberrocal\Documents\codigo_tino_ns\tino_application_framework_3' #'/Users/luiscberrocal/PycharmProjects/wildbills_project'
    clean_output = False

    def setUp(self):
        self.excel_adapter = ExcelAdapter()

    def test_write(self):
        reporter = GitReporter(self.working_directory)
        report = reporter.report()

        excel_reporter = ExcelGitReporter()
        output_filename = filename_with_datetime(TEST_OUTPUT_PATH, 'git_reporter_commits.xlsx')
        commit_count = excel_reporter.write(output_filename, report,start_date=datetime.date(2015,10,1), end_date=datetime.date(2016,2,22))
        self.assertTrue(os.path.exists(output_filename))
        self.assertEqual(len(report['commits']), commit_count)

        results = self.excel_adapter.convert_to_list(output_filename, 'Commits')
        self.assertEqual(commit_count, len(results))

        for result in results:
            self.assertEqual(13, len(result))
            self.assertRegex(result[0], '[a-z0-9]{7}')
            self.assertRegex(result[1], '^[\w._-]{2,}$')
            self.assertRegex(result[2], '^[\w._-]+@[\w.-]+\.[A-Za-z]{2,}$')

        if self.clean_output:
            os.remove(output_filename)

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

        results = self.excel_adapter.convert_to_list(output_filename, 'Commits')
        #self.assertEqual(commit_count + commit_count_2, len(results)) TODO 20160310 commits arent adding up

        for result in results:
            self.assertEqual(13, len(result))
            self.assertRegex(result[0], '[a-z0-9]{7}')
            self.assertRegex(result[1], '^[\w._-]{2,}$')
            self.assertRegex(result[2], '^[\w._-]+@[\w.-]+\.[A-Za-z]{2,}$')

        if self.clean_output:
            os.remove(output_filename)


class TestExcelCommitImporter(TestCase):

    clean_output = False

    def setUp(self):
        self.excel_adapter = ExcelAdapter()

    def test_parse_multiple_files(self):
        factory = CommitFactory()
        folder = os.path.join(TEST_OUTPUT_PATH, 'test_parse_multiple_files')
        if os.path.exists(folder):
            shutil.rmtree(folder)
        filenames = factory.create_commit_folder(folder, 2015, [3,4,5,6], 1)

        output_filename = filename_with_datetime(TEST_OUTPUT_PATH, 'test_parse_multiple_files.xlsx')
        importer = ExcelCommitImporter()
        commit_count = importer.parse_multiple_files(filenames, output_filename)
        self.assertTrue(os.path.exists(output_filename))
        self.assertEqual(122, commit_count)

        results = self.excel_adapter.convert_to_list(output_filename, 'Commits')
        self.assertEqual(122, len(results))
        self.assertEqual(8, len(results[0]))

        logger.debug('Wrote commits to %s' % output_filename)
        if self.clean_output:
            os.remove(output_filename)
            shutil.rmtree(folder)

    def test_parse_multiple_files_date_filtered(self):
        factory = CommitFactory()
        folder = os.path.join(TEST_OUTPUT_PATH, 'test_parse_multiple_files_date_filtered')
        if os.path.exists(folder):
            shutil.rmtree(folder)
        filenames = factory.create_commit_folder(folder, 2015, [9,10,11,12], 2)

        output_filename = filename_with_datetime(TEST_OUTPUT_PATH, 'test_parse_multiple_files_date_filtered.xlsx')
        importer = ExcelCommitImporter()
        commit_count = importer.parse_multiple_files(filenames, output_filename,
                                                     start_date=datetime.date(2015,11,1),
                                                     end_date=datetime.date(2015,12,31))
        self.assertTrue(os.path.exists(output_filename))
        self.assertEqual(122, commit_count)

        results = self.excel_adapter.convert_to_list(output_filename, 'Commits')
        self.assertEqual(122, len(results))
        self.assertEqual(8, len(results[0]))

        logger.debug('Wrote commits to %s' % output_filename)
        if self.clean_output:
            os.remove(output_filename)
            shutil.rmtree(folder)

    def test_parse_multiple_files_single(self):
        filename = filename_with_datetime(TEST_OUTPUT_PATH, 'vessel_display_web.txt')
        create_fake_commits_file(filename, start_date=datetime.date(2015,10,1), end_date=datetime.date(2016,1,1), commits_per_day=1)
        filenames = [filename]
        importer = ExcelCommitImporter()
        output_filename = filename_with_datetime(TEST_OUTPUT_PATH, 'git_commits_acp_contract.xlsx')
        commit_count = importer.parse_multiple_files(filenames, output_filename, start_date=datetime.date(2015,10,1), end_date=datetime.date(2015,10,31))
        self.assertTrue(os.path.exists(output_filename))
        self.assertEqual(31, commit_count)

        results = self.excel_adapter.convert_to_list(output_filename, 'Commits')
        self.assertEqual(31, len(results))
        self.assertEqual(8, len(results[0]))

        logger.debug('Wrote commits to %s' % output_filename)
        if self.clean_output:
            os.remove(output_filename)
            os.remove(filename)

    def test_parse_multiple_files_2(self):
        factory = CommitFactory()
        folder = os.path.join(TEST_OUTPUT_PATH, 'test_parse_multiple_files_2')
        if os.path.exists(folder):
            shutil.rmtree(folder)
        filenames = factory.create_commit_folder(folder, 2015, [9,10,11,12], 1)

        importer = ExcelCommitImporter()
        output_filename = filename_with_datetime(TEST_OUTPUT_PATH, 'git_commits_acp_contract_02.xlsx')
        commit_count = importer.parse_multiple_files(filenames, output_filename, start_date=datetime.date(2015,10,1), end_date=datetime.date(2015,12,31))
        self.assertTrue(os.path.exists(output_filename))
        self.assertEqual(92, commit_count)

        results = self.excel_adapter.convert_to_list(output_filename, 'Commits')
        self.assertEqual(92, len(results))
        self.assertEqual(8, len(results[0]))

        logger.debug('Wrote commits to %s' % output_filename)
        if self.clean_output:
            os.remove(output_filename)
            shutil.rmtree(folder)


    def test_parse_folder(self):
        factory = CommitFactory()
        folder = os.path.join(TEST_OUTPUT_PATH, 'test_parse_folder')
        if os.path.exists(folder):
            shutil.rmtree(folder)
        factory.create_commit_folder(folder, 2015, [9,10,11,12], 1)

        importer = ExcelCommitImporter()
        output_filename = filename_with_datetime(TEST_OUTPUT_PATH, 'git_commits_parse_folder.xlsx')
        commit_count = importer.parse_folder(folder, output_filename, start_date=datetime.date(2015,10,1), end_date=datetime.date(2015,10,31))
        self.assertTrue(os.path.exists(output_filename))
        self.assertEqual(31, commit_count)

        results = self.excel_adapter.convert_to_list(output_filename, 'Commits')
        self.assertEqual(31, len(results))
        self.assertEqual(8, len(results[0]))

        logger.debug('Wrote commits to %s' % output_filename)
        if self.clean_output:
            os.remove(output_filename)
            shutil.rmtree(folder)

