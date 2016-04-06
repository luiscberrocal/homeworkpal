# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('interviews', '0013_auto_20160328_0859'),
    ]

    operations = [
        migrations.AddField(
            model_name='elegibilitycertificate',
            name='date_closed',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='candidate',
            name='national_id',
            field=models.CharField(unique=True, max_length=15),
        ),
        migrations.AlterField(
            model_name='interview',
            name='start_datetime',
            field=models.DateTimeField(default=datetime.datetime(2016, 4, 6, 12, 21, 55, 380427, tzinfo=utc)),
        ),
    ]
