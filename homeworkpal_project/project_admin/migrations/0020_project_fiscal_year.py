# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('project_admin', '0019_projectgoal_update_goal_info'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='fiscal_year',
            field=models.CharField(max_length=4, default='AF16', validators=[django.core.validators.RegexValidator(regex='^AF\\d2$')]),
            preserve_default=False,
        ),
    ]
