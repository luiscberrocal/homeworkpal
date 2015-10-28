# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0004_auto_20151026_1823'),
        ('project_admin', '0004_auto_20151026_0929'),
    ]

    operations = [
        migrations.CreateModel(
            name='Stakeholder',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('rank', models.IntegerField(help_text='Rank of the stakeholder in the project', default=10)),
                ('employee', models.ForeignKey(related_name='projects_as_stakeholder', to='employee.Employee')),
                ('project', models.ForeignKey(related_name='stakeholders', to='project_admin.Project')),
            ],
            options={
                'ordering': ['project', 'rank'],
            },
        ),
    ]
