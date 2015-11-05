# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('project_admin', '0013_auto_20151104_2238'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectmember',
            name='start_date',
            field=models.DateField(default=datetime.datetime(2015, 11, 5, 15, 31, 46, 395842, tzinfo=utc)),
        ),
    ]
