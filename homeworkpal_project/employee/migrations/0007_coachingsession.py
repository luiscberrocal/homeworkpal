# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
from django.utils.timezone import utc
import model_utils.fields
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0006_auto_20151104_2159'),
    ]

    operations = [
        migrations.CreateModel(
            name='CoachingSession',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('created', model_utils.fields.AutoCreatedField(verbose_name='created', editable=False, default=django.utils.timezone.now)),
                ('modified', model_utils.fields.AutoLastModifiedField(verbose_name='modified', editable=False, default=django.utils.timezone.now)),
                ('start_date_time', models.DateTimeField(default=datetime.datetime(2015, 11, 17, 18, 23, 54, 910572, tzinfo=utc))),
                ('end_date_time', models.DateTimeField(null=True, blank=True)),
                ('comments', models.TextField()),
                ('coach', models.ForeignKey(to='employee.Employee', related_name='coached_sessions')),
                ('employee', models.ForeignKey(to='employee.Employee', related_name='coaching_sessions')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
