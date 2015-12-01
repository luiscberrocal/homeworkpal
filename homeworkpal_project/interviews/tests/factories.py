import datetime
import string
from factory import Iterator, lazy_attribute
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyText
from ..models import ElegibilityCertificate

__author__ = 'LBerrocal'


class ElegibilityCertificateFactory(DjangoModelFactory):

    class Meta:
        model = ElegibilityCertificate

    number =  FuzzyText(length=7, chars=string.digits)
    grade = Iterator(['NM-07', 'NM-09', 'NM-11', 'NM-12', 'NM-13'])
    ends_at = datetime.date(2016,9,30)
    emitted = datetime.datetime.now().date()
    salary_per_year = 35251.12

    @lazy_attribute
    def expires(self):
        td = datetime.timedelta(days=30)
        return self.emitted + td
