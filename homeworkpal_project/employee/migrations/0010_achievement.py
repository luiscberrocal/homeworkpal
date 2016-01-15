# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0009_auto_20160104_1418'),
    ]

    operations = [
        migrations.CreateModel(
            name='Achievement',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(editable=False, verbose_name='created', default=django.utils.timezone.now)),
                ('modified', model_utils.fields.AutoLastModifiedField(editable=False, verbose_name='modified', default=django.utils.timezone.now)),
                ('type', models.CharField(max_length=12, choices=[('ACHIEVEMENT', 'Achievement'), ('INITIATIVE', 'Initiative')])),
                ('description', models.TextField()),
                ('date', models.DateField()),
                ('points', models.IntegerField(default=0)),
                ('employee', models.ForeignKey(to='employee.Employee', related_name='achievements')),
                ('evaluator', models.ForeignKey(to='employee.Employee', related_name='achievement_evaluations')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
