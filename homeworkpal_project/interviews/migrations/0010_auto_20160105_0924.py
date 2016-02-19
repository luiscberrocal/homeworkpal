# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('interviews', '0009_auto_20160104_1418'),
    ]

    operations = [
        migrations.AlterField(
            model_name='interview',
            name='start_datetime',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 5, 14, 24, 48, 958347, tzinfo=utc)),
        ),
    ]