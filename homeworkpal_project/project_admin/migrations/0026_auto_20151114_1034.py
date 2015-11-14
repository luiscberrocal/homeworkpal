# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
import django.core.validators
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0006_auto_20151104_2159'),
        ('project_admin', '0025_auto_20151114_0918'),
    ]

    operations = [
        migrations.CreateModel(
            name='IndividualGoal',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('name', models.CharField(null=True, max_length=120)),
                ('description', models.TextField(null=True)),
                ('expectations', models.TextField(null=True)),
                ('weight', models.FloatField(validators=[django.core.validators.MaxValueValidator(1.0), django.core.validators.MinValueValidator(0.0)])),
                ('expected_advancement', models.FloatField(default=0.9, validators=[django.core.validators.MaxValueValidator(1.0), django.core.validators.MinValueValidator(0.0)])),
                ('update_goal_info', models.BooleanField(default=True, help_text='Will update name, description and expectations based on the project information')),
                ('fiscal_year', models.CharField(max_length=4, validators=[django.core.validators.RegexValidator(message='Fiscal year must use format AFYY. For example AF16 for fiscal year 2016', regex='^AF\\d{2}$')])),
                ('employee', models.ForeignKey(to='employee.Employee', related_name='goals')),
                ('project', models.ForeignKey(null=True, to='project_admin.Project')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='projectgoal',
            name='employee',
            field=models.ForeignKey(to='employee.Employee', related_name='project_goals_old'),
        ),
        migrations.AlterField(
            model_name='projectgoal',
            name='fiscal_year',
            field=models.CharField(max_length=4, validators=[django.core.validators.RegexValidator(message='Fiscal year must use format AFYY. For example AF16 for fiscal year 2016', regex='^AF\\d{2}$')]),
        ),
    ]
