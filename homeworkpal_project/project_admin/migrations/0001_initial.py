# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators
import autoslug.fields


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Deliverable',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=120)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('short_name', models.CharField(max_length=60)),
                ('description', models.TextField()),
                ('planned_start_date', models.DateField()),
                ('planned_end_date', models.DateField()),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from=models.CharField(max_length=60), unique=True)),
                ('planned_man_hours', models.DecimalField(decimal_places=2, max_digits=7)),
                ('type', models.CharField(choices=[('PROJECT', 'Proyecto'), ('INTERNAL', 'Interno'), ('SUPPORT', 'Apoyo')], default='PROJECT', max_length=8)),
            ],
        ),
        migrations.CreateModel(
            name='ProjectGoal',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('weight', models.FloatField(validators=[django.core.validators.MaxValueValidator(1.0), django.core.validators.MinValueValidator(0.0)])),
                ('expected_advancement', models.FloatField(validators=[django.core.validators.MaxValueValidator(1.0), django.core.validators.MinValueValidator(0.0)], default=0.9)),
                ('employee', models.ForeignKey(to='employee.Employee')),
                ('project', models.ForeignKey(to='project_admin.Project')),
            ],
        ),
        migrations.AddField(
            model_name='deliverable',
            name='project',
            field=models.ForeignKey(to='project_admin.Project'),
        ),
    ]
