# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import autoslug.fields


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0005_companygroup_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companygroup',
            name='slug',
            field=autoslug.fields.AutoSlugField(editable=False, unique=True, populate_from='name', max_length=10),
        ),
    ]
