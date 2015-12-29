# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0007_coachingsession'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coachingsession',
            name='start_date_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
