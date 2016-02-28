import csv

import pytz
from datetime import timedelta, datetime, date
from faker import Factory as FakerFactory

from common.utils import force_date_to_dateime, Holiday

faker = FakerFactory.create()

class CommitFactory(object):

    tz = pytz.timezone('America/Panama')
    datetime_format = '%a, %d %b %Y %H:%M:%S %z'

    def create(self, **kwargs):
        commit_date = self.tz.localize(faker.date_time_between(start_date="-6m", end_date="now"))
        commit_date = kwargs.get('commit_date', commit_date)
        if isinstance(commit_date, date):
            commit_date = force_date_to_dateime(commit_date, tzinfo=self.tz)

        commit_data = [ faker.md5()[:7],
                        faker.email(),
                        commit_date.strftime(self.datetime_format),
                        faker.sentence(nb_words=6, variable_nb_words=True)]
        return commit_data

    def create_in_date_range(self, start_date, end_date, commits_per_day=2):
        commit_list = list()
        day_generator =  Holiday.days_in_range_generator(start_date, end_date) #(start_date + timedelta(x + 1) for x in range((end_date - start_date).days))
        for day in day_generator:
            for n in range(0, commits_per_day):
                commit_list.append(self.create(commit_date=day))
        return commit_list



def create_fake_commits_file(filename, **kwargs):
    '''
    Creates a file as if you used this git command:

        $ git log --pretty=format:'%h|%ae|%aD|%s' >> filename.pike

    The result from the command should be something like this:

        8e802b5| bbb@pancanal.com     |Mon, 12 Oct 2015 19:43:26 -0500 |Basic model impl
        ad88bc6| bbb@pancanal.com     |Sun, 11 Oct 2015 11:10:08 -0500 |First commit

    :param filename:
    :param commit_count:
    :return:
    '''
    commit_count= kwargs.get('commit_count', 50)
    start_date = kwargs.get('start_date', None)
    end_date = kwargs.get('end_date', None)
    commits_per_day = kwargs.get('commits_per_day', 2)

    commit_factory = CommitFactory()
    with open(filename, 'w', encoding='utf-8') as pike_file:
        writer = csv.writer(pike_file, delimiter='|')
        if start_date and end_date:
            commits = commit_factory.create_in_date_range(start_date, end_date, commits_per_day)
            for commit in commits:
                writer.writerow(commit)
        else:
            for n in range(0, commit_count):
                commit_data =  commit_factory.create()
                writer.writerow(commit_data)
    return commit_count