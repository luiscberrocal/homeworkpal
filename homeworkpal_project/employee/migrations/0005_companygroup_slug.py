# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import autoslug.fields


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0004_auto_20151026_1823'),
    ]

    operations = [
        migrations.AddField(
            model_name='companygroup',
            name='slug',
            field=autoslug.fields.AutoSlugField(default='tino-ns', editable=False, unique=True, populate_from='name'),
            preserve_default=False,
        ),
    ]
