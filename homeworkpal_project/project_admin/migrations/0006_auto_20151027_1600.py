# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import autoslug.fields


class Migration(migrations.Migration):

    dependencies = [
        ('project_admin', '0005_stakeholder'),
    ]

    operations = [
        migrations.CreateModel(
            name='CorporateGoal',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('number', models.CharField(max_length=4, unique=True)),
                ('description', models.TextField()),
                ('fiscal_year', models.IntegerField(default=2015)),
            ],
        ),
        migrations.CreateModel(
            name='CorporateGoalAssignment',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('corporate_goal', models.ForeignKey(related_name='projects', to='project_admin.CorporateGoal')),
            ],
        ),
        migrations.AlterField(
            model_name='deliverable',
            name='project',
            field=models.ForeignKey(related_name='deliverables', to='project_admin.Project'),
        ),
        migrations.AlterField(
            model_name='project',
            name='slug',
            field=autoslug.fields.AutoSlugField(populate_from='short_name', editable=False, max_length=60, unique=True),
        ),
        migrations.AddField(
            model_name='corporategoalassignment',
            name='project',
            field=models.ForeignKey(related_name='corporate_goals', to='project_admin.Project'),
        ),
    ]
