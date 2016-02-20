from django.test import TestCase

from jira_git.git_utils import GitReporter


class TestGitReporter(TestCase):

    working_directory = '/Users/luiscberrocal/PycharmProjects/wildbills_project'

    def test_report(self):
        reporter = GitReporter(self.working_directory)
        report = reporter.report()
        self.assertEqual(120, len(report['commits']))
        self.assertEqual('develop', report['branch'])
        self.assertEqual('git@bitbucket.org:luiscberrocal/wilbills.git', report['repo_name'])

    def test_get_current_branch(self):
        reporter = GitReporter(self.working_directory)
        branch = reporter.get_current_branch()
        self.assertEqual('develop', branch)

    def test_get_repository_name(self):
        reporter = GitReporter(self.working_directory)
        repo_name = reporter.get_repository_name()
        self.assertEqual('git@bitbucket.org:luiscberrocal/wilbills.git', repo_name)
