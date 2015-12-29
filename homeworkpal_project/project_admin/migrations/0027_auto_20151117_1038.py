# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_admin', '0026_auto_20151114_1034'),
    ]

    operations = [
        migrations.AddField(
            model_name='individualgoal',
            name='priority',
            field=models.IntegerField(default=1000, help_text='The lower the number the higher the priority'),
        ),
        migrations.AlterField(
            model_name='individualgoal',
            name='description',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='individualgoal',
            name='expectations',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='individualgoal',
            name='name',
            field=models.CharField(null=True, blank=True, max_length=120),
        ),
        migrations.AlterField(
            model_name='individualgoal',
            name='project',
            field=models.ForeignKey(null=True, blank=True, to='project_admin.Project'),
        ),
    ]
