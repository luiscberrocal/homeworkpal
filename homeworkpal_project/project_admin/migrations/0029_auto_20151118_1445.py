# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_admin', '0028_projectsupport'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectsupport',
            name='tickets',
            field=models.ManyToManyField(null=True, blank=True, to='maximo.MaximoTicket'),
        ),
    ]
