# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('interviews', '0007_auto_20151130_1329'),
    ]

    operations = [
        migrations.AlterField(
            model_name='elegibilitycertificate',
            name='number',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='interview',
            name='start_datetime',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 2, 15, 0, 12, 612358, tzinfo=utc)),
        ),
    ]
