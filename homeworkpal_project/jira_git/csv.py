import csv

import datetime
import re

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

    def parse(self, filename):
        commits = list()
        date_format = '%a, %d %b %Y %H:%M:%S %z'
        with open(filename, 'r', encoding='utf-8') as pike_file:
            reader = csv.reader(pike_file, delimiter='|')
            for row in reader:
                hash = row[0].strip()
                username = self.git_name.get_user(row[1].strip())
                date = datetime.datetime.strptime(row[2].strip(),date_format)
                description = row[3].strip()
                project = self.get_project(description)
                commits.append([hash,  username, date, description, project])
        return commits

    def get_project(self, description, **kwargs):
        for project_tag in GIT_JIRA_PROJECT_TAGS:
            regexp_str = r'.*(%s-\d+)\s?' % project_tag[1] #.*(NAV-\d+)\s?
            logger.debug('Regular expression: %s' % regexp_str)
            regexp = re.compile(regexp_str)
            match = regexp.match(description)
            if match:
                return project_tag[0]



