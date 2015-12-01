# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interviews', '0002_contactattempt_contacted_by'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contactattempt',
            name='candidate',
        ),
        migrations.AlterField(
            model_name='candidate',
            name='middle_name',
            field=models.CharField(max_length=30, blank=True),
        ),
    ]
