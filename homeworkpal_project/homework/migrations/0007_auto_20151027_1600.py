# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import autoslug.fields


class Migration(migrations.Migration):

    dependencies = [
        ('homework', '0006_auto_20151019_0715'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schoollevel',
            name='slug',
            field=autoslug.fields.AutoSlugField(populate_from='name', editable=False, max_length=10, unique=True),
        ),
        migrations.AlterField(
            model_name='subject',
            name='slug',
            field=autoslug.fields.AutoSlugField(populate_from='name', editable=False, max_length=30),
        ),
    ]
