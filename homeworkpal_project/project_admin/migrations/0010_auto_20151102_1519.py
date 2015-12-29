# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('project_admin', '0009_auto_20151101_0847'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectmember',
            name='start_date',
            field=models.DateField(default=datetime.datetime(2015, 11, 2, 20, 18, 58, 634099, tzinfo=utc)),
        ),
    ]
