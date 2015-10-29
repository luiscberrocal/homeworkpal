from datetime import datetime, date

__author__ = 'LBerrocal'


class Holiday(object):
    holidays = (
        date(2015,11,3),
        date(2015,11,5),
        date(2015,11,10),
        date(2015,11,27),
        date(2015,12,8),
        date(2015,12,25),
    )

    def is_holiday(self, date):
        return date in self.holidays