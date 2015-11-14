# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('project_admin', '0023_auto_20151114_0911'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='fiscal_year',
            field=models.CharField(max_length=4, validators=[django.core.validators.RegexValidator(regex='^AF\\d{2}$', message='Fiscal year must us format AFYY. For example AF16 for fiscal year 2016')]),
        ),
    ]
