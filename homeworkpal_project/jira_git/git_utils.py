import os
import re
import subprocess

from common.utils import cd
import logging
logger = logging.getLogger(__name__)

class GitReporter(object):

    def __init__(self, working_directory):
        self.working_directory = working_directory
        assert os.path.exists(os.path.join(self.working_directory, '.git')), '%s working directory is not a git repository' % self.working_directory

    def get_current_branch(self):
        git_command = 'git branch'
        regexp = re.compile(r'^\*\s(.*)')

        branches = self._run_command(git_command)
        for branch in branches:
            match = regexp.match(branch)
            if match:
                return match.group(1)
        return None

    def _run_command(self, git_command):
        # '\\'git\\' is not recognized as an internal or external command,'
        with cd(self.working_directory):
            stdoutdata = subprocess.getoutput(git_command)
            stdoutdata_splited = stdoutdata.split('\n')
            return stdoutdata_splited

    def get_repository_name(self):
        '''
        Will extract repository name from git config --list command
        :return: Fetch URl of repository
        '''
        git_command = 'git config --list'
        regexp = re.compile(r'remote\.origin\.url=(.*)$')
        results = self._run_command(git_command)
        for origin_data in results:
            match = regexp.match(origin_data)
            logger.debug(origin_data)
            if match:
                return match.group(1)
        return None

    def report(self):
        report = dict()
        branch = self.get_current_branch()
        assert branch is not None, 'Could not find a branch for %s' % self.working_directory
        report['branch'] = branch

        repo_name = self.get_repository_name()
        assert repo_name is not None, 'Could not find repository name for %s' % self.working_directory
        report['repo_name'] = repo_name
        git_command = 'git log --pretty=format:"%h| %<(20)%an |%aD |%s"'
        report['commits'] = self._run_command(git_command)

        return report
