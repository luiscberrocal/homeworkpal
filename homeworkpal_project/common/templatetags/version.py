import os
from django import template
import time

__author__ = 'lberrocal'

register = template.Library()


@register.simple_tag
def version_number():
    return '0.6.0'


@register.simple_tag
def version_date():
    return time.strftime('%m/%d/%Y', time.gmtime(os.path.getmtime('../.git')))
