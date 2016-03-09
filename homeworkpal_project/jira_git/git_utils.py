import os
import re
import shlex
import subprocess

import datetime

from common.utils import cd
import logging

from jira_git.excel import ExcelGitReporter

logger = logging.getLogger(__name__)


def create_git_excel(folder, output_filename):
    for root, dirs, files in os.walk(folder):
        for directory in dirs:
            full_path = os.path.join(root, directory)
            git_reporter = GitReporter(full_path)
            report = git_reporter.report()
            excel_reporter = ExcelGitReporter()
            #commit_count = excel_reporter.write(output_filename, report,start_date=datetime.date(2015,10,1), end_date=datetime.date(2016,2,22))
            commit_count = excel_reporter.write(output_filename, report)
            logger.debug('Fullpath: %s: commits %d' % (full_path, commit_count))
        break
    logger.debug('Wrote %s' % output_filename)



class GitReporter(object):
    '''
    This class is designed to extract git commits to create a rerport from a folder.
    '''

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
        results = self._run_command(git_command)
        logger.debug(results)
        #assert len(result) == 2, 'Could not checkout branch %s for working dir %s' % (branch_name, self.working_directory)
        regexp = re.compile(r'^(Switched\sto\sbranch|Already\son)\s\'(.*)\'')
        for result in results:
            match = regexp.match(result)
            if match:
                return branch_name, None

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
                #logger.debug(line)
                stdoutdata_splited.append(line.decode(encoding='utf-8').rstrip('\r\n'))
            return stdoutdata_splited

    def get_repository_info(self):
        regexp = re.compile(r'remote\.origin\.url=(http:\/\/([\w\.-]+)@stash.canal.acp:\d+(.*)(\/([\w_]+))+\/([\w_]+\.git))$')
        git_command = r'git config --list'
        results = self._run_command(git_command)
        for origin_data in results:
            match = regexp.match(origin_data)
            #logger.debug(origin_data)
            if match:
                stash_url = match.group(1)
                stash_project = match.group(5)
                repo_name = match.group(6)
                return stash_url, stash_project, repo_name
        return None, None, None

    def get_repository_name(self):
        '''
        Will extract repository name from git config --list command
        :return: Fetch URl of repository
        '''
        return self.get_repository_info()[0]
        # git_command = r'git config --list'
        # regexp = re.compile(r'remote\.origin\.url=(.*)$')
        # results = self._run_command(git_command)
        # for origin_data in results:
        #     match = regexp.match(origin_data)
        #     #logger.debug(origin_data)
        #     if match:
        #         return match.group(1)
        #return None

    def report(self, number_of_commits=0):
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
        git_command = r'git log --shortstat --pretty=format:"%h|%ae|%aD|%s"'
        if number_of_commits != 0:
            git_command += ' -n %d' % number_of_commits

        lines = self._run_command(git_command)
        report['commits'] = list()
        current_line = 0
        regexp = re.compile(r'(\d+)\sfiles?\schanged,\s(\d+)\sinsertions?\(\+\),\s(\d+)\sdeletions?\(\-\)')
        for line in lines:
            if len(line) == 0:
                current_line += 1
                continue
            match = regexp.findall(line)
            if len(match) != 0:
                commit_details = lines[current_line-1].split('|')
                commit_details.append(match[0][0]) #Files Changed
                commit_details.append(match[0][1]) #Insertions
                commit_details.append(match[0][2]) #Deletions
                report['commits'].append('|'.join(commit_details))
            current_line += 1

        if prev_branch:
            self.checkout_branch(prev_branch)

        return report
