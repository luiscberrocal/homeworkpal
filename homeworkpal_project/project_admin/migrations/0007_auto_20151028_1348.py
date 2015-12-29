# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_admin', '0006_auto_20151027_1600'),
    ]

    operations = [
        migrations.CreateModel(
            name='Risk',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('risk_type', models.CharField(default='THREAT', max_length=12, choices=[('THREAT', 'Amenaza'), ('OPPORTUNITY', 'Oportunidad')])),
                ('priority', models.IntegerField(default=1)),
                ('description', models.TextField()),
                ('project', models.ForeignKey(related_name='risks', to='project_admin.Project')),
            ],
        ),
        migrations.AlterField(
            model_name='corporategoal',
            name='fiscal_year',
            field=models.IntegerField(default=2016),
        ),
    ]
