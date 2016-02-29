import calendar
import csv
import os
import pytz
from datetime import timedelta, datetime, date
from faker import Factory as FakerFactory

from common.utils import force_date_to_dateime, Holiday, filename_with_datetime

faker = FakerFactory.create()

class TagFactory(object):
    '''
    Clas to generate JIRA style tags. For exmpaple JPD-3
    '''

    def create(self, **kwargs):
        length = kwargs.get('length', 3)
        tag_name = kwargs.get('tag_name', None)
        if tag_name is None:
            tag_name = faker.word()
            while len(tag_name) < length:
                tag_name = faker.word()
            tag_name = tag_name[:length].upper()
        number = faker.pyint()
        return '%s-%d' % (tag_name, number)




class CommitFactory(object):

    tz = pytz.timezone('America/Panama')
    datetime_format = '%a, %d %b %Y %H:%M:%S %z'
    tag_factory = TagFactory()

    def create(self, **kwargs):
        commit_date = self.tz.localize(faker.date_time_between(start_date="-6m", end_date="now"))
        commit_date = kwargs.get('commit_date', commit_date)
        if isinstance(commit_date, date):
            commit_date = force_date_to_dateime(commit_date, tzinfo=self.tz)
        description = '%s %s' % (self.tag_factory.create(),  faker.sentence(nb_words=6, variable_nb_words=True))

        commit_data = [ faker.md5()[:7],
                        faker.email(),
                        commit_date.strftime(self.datetime_format),
                        description]
        return commit_data

    def create_in_date_range(self, start_date, end_date, commits_per_day=2):
        commit_list = list()
        day_generator =  Holiday.days_in_range_generator(start_date, end_date) #(start_date + timedelta(x + 1) for x in range((end_date - start_date).days))
        for day in day_generator:
            for n in range(0, commits_per_day):
                commit_list.append(self.create(commit_date=day))
        return commit_list

    def create_commit_folder(self, folder, year, months, commits_per_day=1):
        assert not os.path.exists(folder), 'Folder already %s exists' % folder
        os.makedirs(folder)
        date_ranges = list()
        for month in months:
            data = dict()
            last_day = calendar.monthrange(year,month)[1]
            data['start_date'] = date(year, month, 1)
            data['end_date'] = date(year, month, last_day)
            data['base_filename'] = '%s.pike' % data['start_date'].strftime('%b')
            date_ranges.append(data)

        filenames = list()
        for date_info in date_ranges:
            filename = filename_with_datetime(folder, date_info['base_filename'])
            create_fake_commits_file(filename,
                                     start_date=date_info['start_date'],
                                     end_date=date_info['end_date'],
                                     commits_per_day=commits_per_day)
            filenames.append(filename)
        return filenames




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