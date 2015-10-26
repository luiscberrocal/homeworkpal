# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_admin', '0002_auto_20151025_0529'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='project',
            options={'ordering': ['priority', 'planned_man_hours']},
        ),
        migrations.AddField(
            model_name='project',
            name='priority',
            field=models.IntegerField(default=10, help_text='The lower the number the higher the prriority'),
        ),
    ]
