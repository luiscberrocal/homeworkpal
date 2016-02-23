import csv

import datetime
import re
import os
import pytz

from homeworkpal_project.settings.local_acp import GIT_NAME_DICTIONARY, GIT_JIRA_PROJECT_TAGS
import logging

logger = logging.getLogger(__name__)

class GitName(object):
    '''
    Class to convert git name to a username
    '''

    name_dictionary = GIT_NAME_DICTIONARY

    def get_user(self, name):
        try:
            return self.name_dictionary[name.strip()]
        except KeyError:
            raise ValueError('%s has no user' % name)

class GitExportParser(object):
    '''
    Class to parse files exported using the git command:

        $ git log --pretty=format:'%h| %<(20)%an |%aD |%s'

    The result from the command should be something like this:

        8e802b5| Luis C. Berrocal     |Mon, 12 Oct 2015 19:43:26 -0500 |Basic model impl
        ad88bc6| Luis C. Berrocal     |Sun, 11 Oct 2015 11:10:08 -0500 |First commit
    '''
    def __init__(self):
        self.git_name = GitName()
        self.date_format = '%a, %d %b %Y %H:%M:%S %z'

    def parse_folder(self, folder, **kwargs):
        file_list= list()
        commits = list()
        for root, dir, files in os.walk(folder):
            for file in files:
                filename = os.path.join(root, file)
                #file_list.append(file)
                file_commits = self.parse(filename, **kwargs)
                commits += file_commits
        return commits

    def parse_dictionary(self, dictionary, **kwargs):
        '''
        Parses a dictionary generated with the report method from gis_utils.GitReporter.
        :param dictionary: The dictionary contains
            branch: name of the branch
            repo_name: name of the repository
            commits: commits for the repository
        :return: A list the the parsed commits
        '''

        commits = list()
        for commit_str in dictionary['commits']:
            commit_array = commit_str.split('|')
            commit = self._process_commit(commit_array)
            commits.append(commit + [dictionary['repo_name'], dictionary['branch']])
        return commits

    def _process_commit(self, row, **kwargs):
        date = datetime.datetime.strptime(row[2].strip(),self.date_format)
        passed_filter = self.date_filter(date, kwargs.get('start_date', None), kwargs.get('end_date', None))
        if passed_filter:
            hash_id = row[0].strip()
            username = self.git_name.get_user(row[1].strip())
            description = row[3].strip()
            project, issue_number = self.get_project(description)
            commit_type = self.get_commit_type(description)
            return [hash_id,  username, date, description,
                    project, commit_type, issue_number]
        return None

    def parse(self, filename, **kwargs):
        commits = list()

        with open(filename, 'r', encoding='utf-8') as pike_file:
            logger.debug('Parsing %s' % filename)
            reader = csv.reader(pike_file, delimiter='|')
            _, base_filename = os.path.split(filename)
            for row in reader:
                commit = self._process_commit(row, **kwargs)
                if commit:
                    commits.append(commit + [base_filename])
        return commits

    def _convert_date_to_dateime(self, unconverted_date, tzinfo= pytz.UTC):
        converted_datetime = datetime.datetime(year=unconverted_date.year,
                                           month=unconverted_date.month,
                                           day=unconverted_date.day,
                                           hour = 0,
                                           minute=0,
                                           second=0,
                                           tzinfo=tzinfo)
        return converted_datetime

    def date_filter(self, commit_date, start_date, end_date):
        if start_date is None or end_date is None:
            return True
        if isinstance(start_date, datetime.date):
            start_date = self._convert_date_to_dateime(start_date)
        if isinstance(end_date, datetime.date):
            end_date = self._convert_date_to_dateime(end_date)

        return commit_date >=start_date and commit_date <= end_date

    def get_commit_type(self, description, **kwargs):
        classifiers = [['MERGE', r'^Merge\sbranch\s'],
                       ['RELEASE', r'^Release\sv?(?:(\d+)\.)?(?:(\d+)\.)?(\*|\d+)'],
                       ['KITS', '^Kits\sv?(?:(\d+)\.)?(?:(\d+)\.)?(\*|\d+)']]
        for classifier in classifiers:
            regexp = re.compile(classifier[1])
            match = regexp.match(description)
            if match:
                return classifier[0]

        return 'COMMIT'

    def get_project(self, description, **kwargs):
        for project_tag in GIT_JIRA_PROJECT_TAGS:
            regexp_str = r'.*(%s-\d+).*' % project_tag[1] #.*(NAV-\d+)\s?
            logger.debug('Regular expression: %s' % regexp_str)
            regexp = re.compile(regexp_str)
            match = regexp.match(description)
            if match:
                return project_tag[0], match.group(1)

        return None, None



