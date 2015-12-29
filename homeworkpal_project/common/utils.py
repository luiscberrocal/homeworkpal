import datetime
import os
from django.utils import timezone
from datetime import datetime, date, timedelta

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
        day_generator = (start_date + timedelta(x + 1) for x in range((end_date - start_date).days))
        working_days = sum(1 for day in day_generator if day.weekday() < 5 and not self.is_holiday(day))
        return working_days