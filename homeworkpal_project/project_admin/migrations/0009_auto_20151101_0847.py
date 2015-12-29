# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('project_admin', '0008_auto_20151029_1125'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='risk',
            options={'ordering': ('priority', '-risk_type')},
        ),
        migrations.AlterField(
            model_name='projectmember',
            name='start_date',
            field=models.DateField(default=datetime.datetime(2015, 11, 1, 13, 47, 37, 604121, tzinfo=utc)),
        ),
    ]
