# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('project_admin', '0020_project_fiscal_year'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectgoal',
            name='fiscal_year',
            field=models.CharField(max_length=4, validators=[django.core.validators.RegexValidator(regex='^AF\\d2$')], default='AF16'),
            preserve_default=False,
        ),
    ]
