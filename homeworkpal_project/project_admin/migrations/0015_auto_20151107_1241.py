# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('project_admin', '0014_auto_20151105_1031'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectmember',
            name='start_date',
            field=models.DateField(default=datetime.datetime(2015, 11, 7, 17, 41, 28, 380795, tzinfo=utc)),
        ),
    ]
