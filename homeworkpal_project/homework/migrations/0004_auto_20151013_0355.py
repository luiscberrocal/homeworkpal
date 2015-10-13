# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import homework.validators


class Migration(migrations.Migration):

    dependencies = [
        ('homework', '0003_student'),
    ]

    operations = [
        migrations.AlterField(
            model_name='homework',
            name='due_date',
            field=models.DateField(validators=[homework.validators.date_not_past]),
        ),
        migrations.AlterUniqueTogether(
            name='schoollevel',
            unique_together=set([('name', 'school')]),
        ),
    ]
