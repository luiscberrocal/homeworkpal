# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_admin', '0018_auto_20151113_1702'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectgoal',
            name='update_goal_info',
            field=models.BooleanField(default=True, help_text='Will update name, description and expectations based on the project information'),
        ),
    ]
