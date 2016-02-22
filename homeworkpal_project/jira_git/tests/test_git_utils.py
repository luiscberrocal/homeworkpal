from django.test import TestCase

from homeworkpal_project.settings.local_acp import STASH_HOST, STASH_USERNAME
from jira_git.git_utils import GitReporter


class TestGitReporter(TestCase):

    working_directory = r'C:\Users\lberrocal\Documents\codigo_tino_ns\tino_application_framework_3' #'/Users/luiscberrocal/PycharmProjects/wildbills_project'
    stash_url = 'http://%s@%s' % (STASH_USERNAME, STASH_HOST)

    def test_report(self):
        reporter = GitReporter(self.working_directory)
        report = reporter.report()
        self.assertEqual(192, len(report['commits']))
        self.assertEqual('master', report['branch'])
        #self.assertEqual('git@bitbucket.org:luiscberrocal/wilbills.git', report['repo_name'])
        self.assertEqual('%s/scm/tinons/tino_application_framework_3.git' % self.stash_url, report['repo_name'])

    def test_get_current_branch(self):
        reporter = GitReporter(self.working_directory)
        branch = reporter.get_current_branch()
        self.assertEqual('master', branch)

    def test_get_repository_name(self):
        reporter = GitReporter(self.working_directory)
        repo_name = reporter.get_repository_name()
        self.assertEqual('%s/scm/tinons/tino_application_framework_3.git' % self.stash_url, repo_name)
