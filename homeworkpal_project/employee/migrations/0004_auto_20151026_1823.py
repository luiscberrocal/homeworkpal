# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0003_position_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='position',
            name='owner',
            field=models.OneToOneField(blank=True, null=True, related_name='permanent_position', to='employee.Employee'),
        ),
    ]
