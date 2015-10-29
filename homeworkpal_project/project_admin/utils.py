from datetime import datetime, date

__author__ = 'LBerrocal'


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

    def is_holiday(self, date):
        return date in self.holidays