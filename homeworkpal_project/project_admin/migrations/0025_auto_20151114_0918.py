# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('project_admin', '0024_auto_20151114_0915'),
    ]

    operations = [
        migrations.AlterField(
            model_name='corporategoal',
            name='fiscal_year',
            field=models.CharField(validators=[django.core.validators.RegexValidator(message='Fiscal year must us format AFYY. For example AF16 for fiscal year 2016', regex='^AF\\d{2}$')], max_length=4),
        ),
        migrations.AlterField(
            model_name='projectgoal',
            name='fiscal_year',
            field=models.CharField(validators=[django.core.validators.RegexValidator(message='Fiscal year must us format AFYY. For example AF16 for fiscal year 2016', regex='^AF\\d{2}$')], max_length=4),
        ),
    ]
