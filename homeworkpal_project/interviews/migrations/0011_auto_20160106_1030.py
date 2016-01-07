# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('interviews', '0010_auto_20160105_0924'),
    ]

    operations = [
        migrations.AlterField(
            model_name='interview',
            name='start_datetime',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 6, 15, 30, 22, 278428, tzinfo=utc)),
        ),
    ]
