
from __future__ import absolute_import

import os

from celery import Celery
__author__ = 'lberrocal'
# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'homework_pal_project.settings.local_acp')

from django.conf import settings  # noqa

app = Celery('homework_pal_project')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS, related_name='tasks')

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
