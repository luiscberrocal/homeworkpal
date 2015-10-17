# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import autoslug.fields


class Migration(migrations.Migration):

    dependencies = [
        ('homework', '0004_auto_20151013_0355'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='school',
            field=models.ForeignKey(default=1, to='homework.School'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='student',
            name='school_level',
            field=models.ForeignKey(default=1, to='homework.SchoolLevel'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='school',
            name='slug',
            field=autoslug.fields.AutoSlugField(unique=True, editable=False, populate_from='name'),
        ),
        migrations.AlterField(
            model_name='schoollevel',
            name='slug',
            field=autoslug.fields.AutoSlugField(unique=True, editable=False, populate_from='name'),
        ),
        migrations.AlterField(
            model_name='subject',
            name='slug',
            field=autoslug.fields.AutoSlugField(unique=True, editable=False, populate_from='name'),
        ),
    ]
