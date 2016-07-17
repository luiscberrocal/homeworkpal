import calendar
import datetime
import os

import pytz
from django.utils import timezone
from datetime import datetime, date, timedelta
import time

__author__ = 'lberrocal'


def get_fiscal_year(cdate):
    #year = str(cdate.year)
    if isinstance(cdate, datetime):
        cdate = cdate.date()
    start_of_fy = date(cdate.year, 10,1)
    if cdate >= start_of_fy:
        year = cdate.year + 1
    else:
        year = cdate.year
    return 'AF%s' % str(year)[2:]


def filename_with_datetime(file_path, base_filename):
    '''
    os.path.join(TEST_OUTPUT_PATH, '%s_%s.xlsx' % ('maximo_tickets', timezone.now().strftime('%Y%m%d_%H%M')))
    :param file_path:
    :param base_filename:
    :return:
    '''
    parts = base_filename.split('.')
    if len(parts) > 2:
        raise ValueError('Base filename cannot contain more the one dot')
    str_date = timezone.localtime(timezone.now()).strftime('%Y%m%d_%H%M')
    return os.path.join(file_path, '%s_%s.%s' % (parts[0], str_date, parts[1]))


def add_date_to_filename(filename, **kwargs):
    new_filename = dict()
    #path_parts = filename.split(os.path.se)
    if '/' in filename and '\\' in filename:
        raise ValueError('Filename %s contains both / and \\ separators' % filename)
    if '\\' in filename:
        path_parts = filename.split('\\')
        file = path_parts[-1]
        path = '\\'.join(path_parts[:-1])
        separator = '\\'
    elif '/' in filename:
        path_parts = filename.split('/')
        file = path_parts[-1]
        path = '/'.join(path_parts[:-1])
        separator = '/'
    else:
        file=filename
        path = ''
        separator = ''

    new_filename['path'] = path
    parts = file.split('.')
    new_filename['extension'] = parts[-1]
    new_filename['separator'] = separator
    new_filename['filename_with_out_extension'] = '.'.join(parts[:-1])
    new_filename['datetime'] = timezone.localtime(timezone.now()).strftime('%Y%m%d_%H%M')
    date_position = kwargs.get('date_position', 'suffix')
    if date_position=='suffix':
        return '{path}{separator}{filename_with_out_extension}_{datetime}.{extension}'.format(**new_filename)
    else:
        return '{path}{separator}{datetime}_{filename_with_out_extension}.{extension}'.format(**new_filename)



class Holiday(object):
    holidays = (
        date(2015, 11, 3),
        date(2015, 11, 5),
        date(2015, 11, 10),
        date(2015, 11, 27),
        date(2015, 12, 8),
        date(2015, 12, 25),
        date(2016, 1, 1),
        date(2016, 1, 8),
        date(2016, 2, 9),
        date(2016, 3, 25),
        date(2016, 5, 2),
        date(2016, 11, 3),
        date(2016, 11, 4),
        date(2016, 11, 10),
        date(2016, 11, 28),
        date(2016, 12, 8),
        date(2016, 12, 26),
    )

    def is_holiday(self, event_date):
        return event_date in self.holidays

    def working_days_between(self, start_date, end_date):
        day_generator = Holiday.days_in_range_generator(start_date, end_date) #(start_date + timedelta(x + 1) for x in range((end_date - start_date).days))
        working_days = sum(1 for day in day_generator if day.weekday() < 5 and not self.is_holiday(day))
        return working_days

    def working_days_for_fiscal_year(self, fiscal_year):
        working_days = list()
        months =[(fiscal_year-1, 10),
                 (fiscal_year-1, 11),
                 (fiscal_year-1, 12),
                 (fiscal_year, 1),
                 (fiscal_year, 2),
                 (fiscal_year, 3),
                 (fiscal_year, 4),
                 (fiscal_year, 5),
                 (fiscal_year, 6),
                 (fiscal_year, 7),
                 (fiscal_year, 8),
                 (fiscal_year, 9)]
        for month in months:
            data = dict()
            last_day = calendar.monthrange(month[0],month[1])[1]
            data['start_date'] = date(month[0],month[1], 1)
            data['end_date'] = date(month[0],month[1], last_day)
            data['month'] = data['start_date'].strftime('%b-%Y')
            data['working_days'] = self.working_days_between(data['start_date'], data['end_date'])
            working_days.append(data)
        return working_days

    @staticmethod
    def days_in_range_generator(start_date, end_date):
        start_date = start_date - timedelta(1)
        day_generator = (start_date + timedelta(x + 1) for x in range((end_date - start_date).days))
        return day_generator


class cd:
    """Context manager for changing the current working directory"""
    def __init__(self, newPath):
        self.newPath = os.path.expanduser(newPath)

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)


def force_date_to_dateime(unconverted_date, tzinfo= pytz.UTC):
    converted_datetime = datetime(year=unconverted_date.year,
                                           month=unconverted_date.month,
                                           day=unconverted_date.day,
                                           hour = 0,
                                           minute=0,
                                           second=0,
                                           tzinfo=tzinfo)
    return converted_datetime


class Timer(object):
    def __init__(self, func=time.perf_counter):
        self.elapsed = 0.0
        self._func = func
        self._start = None

    def start(self):
        if self._start is not None:
            raise RuntimeError('Already started')
        self._start = self._func()

    def stop(self):
        if self._start is None:
            raise RuntimeError('Not started')
        end = self._func()
        self.elapsed += end - self._start
        self._start = None

    def reset(self):
        self.elapsed = 0.0

    def get_elapsed_time(self):
        hours, remainder = divmod(self.elapsed, 3600)
        mins, secs = divmod(remainder, 60)
        return int(hours), int(mins), secs

    @property
    def running(self):
        return self._start is not None

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, *args):
        self.stop()