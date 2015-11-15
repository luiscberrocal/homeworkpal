import datetime
import os
from django.utils import timezone

__author__ = 'lberrocal'


def get_fiscal_year(cdate):
    #year = str(cdate.year)
    if isinstance(cdate, datetime.datetime):
        cdate = cdate.date()
    start_of_fy = datetime.date(cdate.year, 10,1)
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


