# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('maximo', '0006_auto_20151111_2021'),
    ]

    operations = [
        migrations.AlterField(
            model_name='maximoticket',
            name='number',
            field=models.CharField(validators=[django.core.validators.RegexValidator(regex='\\d{5,6}')], max_length=7),
        ),
    ]
