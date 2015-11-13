# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('project_admin', '0016_auto_20151111_2021'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectgoal',
            name='project',
            field=models.ForeignKey(to='project_admin.Project', null=True),
        ),
        migrations.AlterField(
            model_name='projectmember',
            name='start_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
