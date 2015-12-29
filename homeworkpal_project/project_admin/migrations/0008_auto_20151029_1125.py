# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0004_auto_20151026_1823'),
        ('project_admin', '0007_auto_20151028_1348'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectMember',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(default='MEMBER', max_length=15, choices=[('MEMBER', 'Team Member'), ('LEADER', 'Team Leader'), ('PRODUCT_OWNER', 'Product Owner')])),
                ('start_date', models.DateField(default=datetime.datetime(2015, 10, 29, 16, 25, 2, 287357, tzinfo=utc))),
                ('end_date', models.DateField(null=True, blank=True)),
                ('employee', models.ForeignKey(to='employee.Employee', related_name='projects')),
            ],
        ),
        migrations.AddField(
            model_name='project',
            name='actual_end_date',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='project',
            name='actual_start_date',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='projectmember',
            name='project',
            field=models.ForeignKey(to='project_admin.Project', related_name='members'),
        ),
    ]
