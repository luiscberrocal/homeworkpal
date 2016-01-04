# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_admin', '0030_auto_20151202_1000'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectmember',
            name='start_date',
            field=models.DateField(),
        ),
    ]
