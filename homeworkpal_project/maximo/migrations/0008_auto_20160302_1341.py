# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maximo', '0007_auto_20151117_1038'),
    ]

    operations = [
        migrations.AlterField(
            model_name='maximoticket',
            name='ticket_type',
            field=models.CharField(choices=[('SR', 'Service Request'), ('WO', 'Work Order'), ('INCIDENT', 'Incident')], default='SR', max_length=8),
        ),
    ]
