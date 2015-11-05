# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maximo', '0003_auto_20151104_2238'),
    ]

    operations = [
        migrations.AddField(
            model_name='maximotimeregister',
            name='pay_rate',
            field=models.DecimalField(decimal_places=2, default=15.0, max_digits=5),
            preserve_default=False,
        ),
    ]
