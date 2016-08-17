# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_admin', '0031_auto_20160104_1418'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='on_dashboard',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
    ]
