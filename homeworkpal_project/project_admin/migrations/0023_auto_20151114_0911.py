# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('project_admin', '0022_auto_20151114_0851'),
    ]

    operations = [
        migrations.AddField(
            model_name='corporategoal',
            name='name',
            field=models.CharField(max_length=120, default='Bla Bla Bla'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='corporategoal',
            name='fiscal_year',
            field=models.CharField(validators=[django.core.validators.RegexValidator(regex='^AF\\d2$')], max_length=4),
        ),
    ]
