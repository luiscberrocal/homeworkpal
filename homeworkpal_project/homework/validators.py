from django.core.exceptions import ValidationError

__author__ = 'luiscberrocal'
from datetime import date

def ∫(value):
    now = date.today()
    if (value < now):
        raise ValidationError('Date cannot be in the past')
