# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_admin', '0017_auto_20151113_1542'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectgoal',
            name='description',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='projectgoal',
            name='expectations',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='projectgoal',
            name='name',
            field=models.CharField(null=True, max_length=120),
        ),
    ]
