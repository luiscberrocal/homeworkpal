# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('interviews', '0012_auto_20160302_1341'),
    ]

    operations = [
        migrations.AlterField(
            model_name='interview',
            name='start_datetime',
            field=models.DateTimeField(default=datetime.datetime(2016, 3, 28, 13, 59, 51, 528747, tzinfo=utc)),
        ),
    ]
