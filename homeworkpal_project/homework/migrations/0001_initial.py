# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import autoslug.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Homework',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('due_date', models.DateField()),
                ('description', models.TextField()),
                ('evaluation', models.CharField(max_length=3, choices=[('SUM', 'Summative'), ('FRM', 'Formative')])),
            ],
        ),
        migrations.CreateModel(
            name='School',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=100)),
                ('slug', autoslug.fields.AutoSlugField(populate_from='name', editable=False)),
            ],
        ),
        migrations.CreateModel(
            name='SchoolLevel',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=10)),
                ('slug', autoslug.fields.AutoSlugField(populate_from='name', editable=False)),
                ('school', models.ForeignKey(to='homework.School')),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=30)),
                ('slug', autoslug.fields.AutoSlugField(populate_from='name', editable=False)),
                ('school_level', models.ForeignKey(to='homework.SchoolLevel')),
            ],
        ),
        migrations.AddField(
            model_name='homework',
            name='subject',
            field=models.ForeignKey(to='homework.Subject'),
        ),
    ]
