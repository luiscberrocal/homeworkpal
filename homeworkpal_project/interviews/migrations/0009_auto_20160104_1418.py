# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('interviews', '0008_auto_20151202_1000'),
    ]

    operations = [
        migrations.AlterField(
            model_name='interview',
            name='start_datetime',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 4, 19, 18, 56, 103880, tzinfo=utc)),
        ),
    ]
