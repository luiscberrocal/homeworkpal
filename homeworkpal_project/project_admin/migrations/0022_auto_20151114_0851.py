# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_admin', '0021_projectgoal_fiscal_year'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectgoal',
            name='employee',
            field=models.ForeignKey(to='employee.Employee', related_name='goals'),
        ),
    ]
