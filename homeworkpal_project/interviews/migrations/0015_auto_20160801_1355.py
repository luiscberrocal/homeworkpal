# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('interviews', '0014_auto_20160406_0721'),
    ]

    operations = [
        migrations.AlterField(
            model_name='interview',
            name='start_datetime',
            field=models.DateTimeField(default=datetime.datetime(2016, 8, 1, 18, 55, 10, 9443, tzinfo=utc)),
        ),
    ]
