from django.test import TestCase

from homeworkpal_project.settings.local_acp import STASH_HOST, STASH_USERNAME
from jira_git.git_utils import GitReporter
import logging

logger = logging.getLogger(__name__)


class TestGitReporter(TestCase):

    working_directory = r'C:\Users\lberrocal\Documents\codigo_tino_ns\tino_application_framework_3' #'/Users/luiscberrocal/PycharmProjects/wildbills_project'
    stash_url = 'http://%s@%s' % (STASH_USERNAME, STASH_HOST)

    def test_report(self):
        reporter = GitReporter(self.working_directory)
        report = reporter.report()
        for commit in report['commits']:
            logger.debug(commit)
        self.assertEqual(190, len(report['commits']))
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

    # def test_checkout_branch(self):
    #     wd = r'C:\Users\lberrocal\Documents\codigo_tino_ns\vessel_display_web_datalayer'
    #     reporter = GitReporter(wd)
    #     branch, updated = reporter.checkout_branch('develop')
    #     self.assertEqual(branch, 'develop')
