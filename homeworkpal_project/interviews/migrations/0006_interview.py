# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.utils.timezone import utc
import datetime
import model_utils.fields
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0008_auto_20151117_1324'),
        ('interviews', '0005_auto_20151126_1559'),
    ]

    operations = [
        migrations.CreateModel(
            name='Interview',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('created', model_utils.fields.AutoCreatedField(verbose_name='created', default=django.utils.timezone.now, editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(verbose_name='modified', default=django.utils.timezone.now, editable=False)),
                ('start_datetime', models.DateTimeField(default=datetime.datetime(2015, 11, 30, 12, 47, 45, 327026, tzinfo=utc))),
                ('end_datetime', models.DateTimeField(null=True, blank=True)),
                ('comments', models.TextField()),
                ('candidate_certificate', models.ForeignKey(related_name='interviews', to='interviews.CandidateInCertificate')),
                ('interviewers', models.ManyToManyField(to='employee.Employee')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
