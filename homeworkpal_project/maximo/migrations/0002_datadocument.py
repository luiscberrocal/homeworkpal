# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import model_utils.fields
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('maximo', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DataDocument',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('docfile', models.FileField(upload_to='maximo_documents/%Y/%m/%d')),
                ('processed', models.DateTimeField()),
                ('extension', models.CharField(max_length=5)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
