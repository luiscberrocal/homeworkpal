# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0008_auto_20151117_1324'),
        ('maximo', '0007_auto_20151117_1038'),
        ('project_admin', '0027_auto_20151117_1038'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectSupport',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(editable=False, default=django.utils.timezone.now, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(editable=False, default=django.utils.timezone.now, verbose_name='modified')),
                ('required_date', models.DateField(blank=True, null=True)),
                ('description', models.TextField()),
                ('company_group', models.ForeignKey(related_name='supports', to='employee.CompanyGroup')),
                ('project', models.ForeignKey(related_name='supports', to='project_admin.Project')),
                ('tickets', models.ManyToManyField(to='maximo.MaximoTicket')),
            ],
            options={
                'ordering': ['project', 'required_date'],
            },
        ),
    ]
