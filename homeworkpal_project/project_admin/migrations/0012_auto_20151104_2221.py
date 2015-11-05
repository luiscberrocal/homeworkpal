# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('project_admin', '0011_auto_20151104_2159'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectmember',
            name='start_date',
            field=models.DateField(default=datetime.datetime(2015, 11, 5, 3, 21, 30, 47558, tzinfo=utc)),
        ),
    ]
