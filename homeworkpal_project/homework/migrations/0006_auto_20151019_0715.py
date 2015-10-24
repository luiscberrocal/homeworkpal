# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import autoslug.fields


class Migration(migrations.Migration):

    dependencies = [
        ('homework', '0005_auto_20151017_0614'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subject',
            name='slug',
            field=autoslug.fields.AutoSlugField(editable=False, populate_from='name'),
        ),
        migrations.AlterUniqueTogether(
            name='subject',
            unique_together=set([('slug', 'school_level')]),
        ),
    ]
