# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('interviews', '0006_interview'),
    ]

    operations = [
        migrations.AddField(
            model_name='candidateincertificate',
            name='explanation',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='interview',
            name='start_datetime',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 30, 18, 29, 13, 655145, tzinfo=utc)),
        ),
    ]
