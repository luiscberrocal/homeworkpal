import datetime

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
