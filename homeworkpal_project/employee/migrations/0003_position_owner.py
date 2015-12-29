# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0002_auto_20151025_1140'),
    ]

    operations = [
        migrations.AddField(
            model_name='position',
            name='owner',
            field=models.OneToOneField(null=True, to='employee.Employee', blank=True),
        ),
    ]
