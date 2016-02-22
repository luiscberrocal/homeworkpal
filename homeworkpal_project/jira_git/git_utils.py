import os
import re
import shlex
import subprocess

from common.utils import cd
import logging
logger = logging.getLogger(__name__)


class GitReporter(object):

    def __init__(self, working_directory, reporting_branch='develop'):
        self.working_directory = working_directory
        self.reporting_branch = reporting_branch
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

    def checkout_branch(self, branch_name):
        git_command = 'git checkout %s' % branch_name
        result = self._run_command(git_command)
        regexp = re.compile(r'^(Switched\sto\sbranch|Already\son)\s\'(.*)\'')
        match = regexp.match(result[1])
        if match:
            return branch_name, True
        else:
            return None, None


    def _run_command(self, git_command):
        # '\\'git\\' is not recognized as an internal or external command,'
        if isinstance(git_command, str):
            arguments = shlex.split(git_command)
        elif isinstance(git_command, list):
            arguments = git_command
        else:
            raise ValueError('git_command must be a string or a list')
        stdoutdata_splited = list()
        with cd(self.working_directory):
            p = subprocess.Popen(arguments , shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            for line in p.stdout.readlines():
                logger.debug(line)
                stdoutdata_splited.append(line.decode(encoding='utf-8').rstrip('\r\n'))
            return stdoutdata_splited

    def get_repository_name(self):
        '''
        Will extract repository name from git config --list command
        :return: Fetch URl of repository
        '''
        git_command = r'git config --list'
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

        prev_branch = None
        if branch != self.reporting_branch:
            prev_branch = branch
            branch, updated =self.checkout_branch(self.reporting_branch)
            assert branch is not None, 'Could not checkout branch %s' % self.reporting_branch
        report['branch'] = branch

        repo_name = self.get_repository_name()
        assert repo_name is not None, 'Could not find repository name for %s' % self.working_directory
        report['repo_name'] = repo_name
        #git_command = ['git', 'log', r'--pretty=format:"%h|%an|%aD|%s"']
        git_command = r'git log --pretty=format:"%h|%an|%aD|%s"'
        report['commits'] = self._run_command(git_command)

        if prev_branch:
            self.checkout_branch(prev_branch)

        return report
