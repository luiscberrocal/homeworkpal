# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('interviews', '0003_auto_20151126_0934'),
    ]

    operations = [
        migrations.CreateModel(
            name='CertificateResult',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(verbose_name='created', default=django.utils.timezone.now, editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(verbose_name='modified', default=django.utils.timezone.now, editable=False)),
                ('action', models.CharField(max_length=3)),
                ('description', models.TextField()),
                ('observations', models.TextField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='candidateincertificate',
            name='certificate_result',
            field=models.ForeignKey(to='interviews.CertificateResult', null=True),
        ),
    ]
