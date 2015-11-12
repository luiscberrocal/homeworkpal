# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maximo', '0005_auto_20151107_1241'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='datadocument',
            options={'ordering': ('-date_start_processing',)},
        ),
    ]
