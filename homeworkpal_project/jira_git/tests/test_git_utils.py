import os

from django.test import TestCase

from common.utils import filename_with_datetime
from homeworkpal_project.settings.base import TEST_OUTPUT_PATH
from homeworkpal_project.settings.local_acp import STASH_HOST, STASH_USERNAME
from jira_git.git_utils import GitReporter, create_git_excel
import logging

logger = logging.getLogger(__name__)


class TestGitReporter(TestCase):
    base_path = r'C:\Users\lberrocal\Documents\codigo_tino_ns'

    stash_url = 'http://%s@%s' % (STASH_USERNAME, STASH_HOST)

    def setUp(self):
        self.working_directory = os.path.join(self.base_path, r'tino_application_framework_3') #'/Users/luiscberrocal/PycharmProjects/wildbills_project'

    def test_report(self):
        reporter = GitReporter(self.working_directory)
        report = reporter.report()
        for commit in report['commits']:
            logger.debug(commit)
            self.assertEqual(7, len(commit.split('|')))
        self.assertEqual('develop', report['branch'])
        #self.assertEqual('git@bitbucket.org:luiscberrocal/wilbills.git', report['repo_name'])
        self.assertEqual('%s/scm/tinons/tino_application_framework_3.git' % self.stash_url, report['repo_name'])

    def test_get_current_branch(self):
        reporter = GitReporter(self.working_directory)
        branch = reporter.get_current_branch()
        self.assertEqual('develop', branch)

    def test_get_repository_name(self):
        reporter = GitReporter(self.working_directory)
        repo_name = reporter.get_repository_name()
        self.assertEqual('%s/scm/tinons/tino_application_framework_3.git' % self.stash_url, repo_name)

    def test_checkout_branch(self):
        wd = os.path.join(self.base_path, r'navigation_aids_app') # vessel_display_web_datalayer
        reporter = GitReporter(wd)
        branch, updated = reporter.checkout_branch('develop')
        self.assertEqual(branch, 'develop')

    def test_get_repository_info(self):
        reporter = GitReporter(self.working_directory)
        url, project, repo = reporter.get_repository_info()
        self.assertEqual('%s/scm/tinons/tino_application_framework_3.git' % self.stash_url, url)
        self.assertEqual('tinons', project)
        self.assertEqual('tino_application_framework_3.git', repo)

    # def test_create_git_excel(self):
    #     output_filename = filename_with_datetime(TEST_OUTPUT_PATH, 'codigo_tino_ns.xlsx')
    #     filename = create_git_excel(self.base_path, output_filename)
