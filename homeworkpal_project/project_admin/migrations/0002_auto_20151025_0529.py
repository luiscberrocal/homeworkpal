# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import autoslug.fields


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0001_initial'),
        ('project_admin', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='group',
            field=models.ForeignKey(null=True, to='employee.CompanyGroup'),
        ),
        migrations.AlterField(
            model_name='project',
            name='slug',
            field=autoslug.fields.AutoSlugField(populate_from='short_name', unique=True, editable=False),
        ),
    ]
