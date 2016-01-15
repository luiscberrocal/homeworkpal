# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0008_auto_20151117_1324'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='coachingsession',
            options={'ordering': ('start_date_time',)},
        ),
    ]
