# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maximo', '0002_datadocument'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datadocument',
            name='processed',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
