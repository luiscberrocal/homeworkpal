# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0008_auto_20151117_1324'),
        ('interviews', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='contactattempt',
            name='contacted_by',
            field=models.ForeignKey(to='employee.Employee', default=1),
            preserve_default=False,
        ),
    ]
