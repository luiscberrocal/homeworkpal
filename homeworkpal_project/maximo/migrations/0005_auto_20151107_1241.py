# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('maximo', '0004_maximotimeregister_pay_rate'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='datadocument',
            name='processed',
        ),
        migrations.AddField(
            model_name='datadocument',
            name='date_end_processing',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='datadocument',
            name='date_start_processing',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='datadocument',
            name='results',
            field=jsonfield.fields.JSONField(null=True),
        ),
        migrations.AddField(
            model_name='datadocument',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Processed', 'Processed'), ('Failed', 'Failed')], default='Pending', max_length=64),
        ),
    ]
