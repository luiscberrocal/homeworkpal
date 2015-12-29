# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import model_utils.fields
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Candidate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('national_id', models.CharField(max_length=15)),
                ('first_name', models.CharField(max_length=30)),
                ('middle_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CandidateInCertificate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('score', models.DecimalField(decimal_places=2, max_digits=5)),
                ('candidate', models.ForeignKey(to='interviews.Candidate', related_name='certificates')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ContactAttempt',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('succesful_contact', models.BooleanField()),
                ('contact_datetime', models.DateTimeField()),
                ('comments', models.TextField()),
                ('candidate', models.ForeignKey(to='interviews.CandidateInCertificate')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ContactInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('number', models.CharField(blank=True, max_length=15)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('instructions', models.TextField(blank=True)),
                ('comments', models.TextField(blank=True)),
                ('valid', models.BooleanField(default=True)),
                ('candidate', models.ForeignKey(to='interviews.Candidate', related_name='contact_info')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ElegibilityCertificate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('number', models.CharField(max_length=100)),
                ('grade', models.CharField(max_length=5)),
                ('ends_at', models.DateField()),
                ('vacant_positions', models.PositiveIntegerField(default=1)),
                ('emitted', models.DateField()),
                ('expires', models.DateField()),
                ('salary_per_year', models.DecimalField(decimal_places=2, max_digits=8)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='contactattempt',
            name='contact_method',
            field=models.ForeignKey(to='interviews.ContactInfo'),
        ),
        migrations.AddField(
            model_name='candidateincertificate',
            name='certificate',
            field=models.ForeignKey(to='interviews.ElegibilityCertificate', related_name='candidates'),
        ),
    ]
