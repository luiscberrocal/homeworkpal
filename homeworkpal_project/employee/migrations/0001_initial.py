# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(unique=True, max_length=10)),
                ('description', models.CharField(blank=True, null=True, max_length=120)),
                ('parent_group', models.ForeignKey(blank=True, null=True, to='employee.CompanyGroup')),
            ],
        ),
        migrations.CreateModel(
            name='CompanyGroupEmployeeAssignment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('middle_name', models.CharField(blank=True, null=True, max_length=30)),
                ('company_id', models.CharField(max_length=7)),
                ('tenure', models.CharField(choices=[('PERM', 'Permanent'), ('TEMP', 'Temporary')], max_length=4)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('number', models.CharField(unique=True, max_length=6)),
                ('grade', models.CharField(max_length=5)),
                ('type', models.CharField(choices=[('PERM', 'Permanent'), ('TEMP', 'Temporary')], max_length=4)),
            ],
        ),
        migrations.CreateModel(
            name='PositionAssignment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField(null=True, blank=True)),
                ('employee', models.ForeignKey(to='employee.Employee')),
                ('position', models.ForeignKey(to='employee.Position')),
            ],
        ),
        migrations.AddField(
            model_name='companygroupemployeeassignment',
            name='employee',
            field=models.ForeignKey(to='employee.Employee'),
        ),
        migrations.AddField(
            model_name='companygroupemployeeassignment',
            name='group',
            field=models.ForeignKey(to='employee.CompanyGroup'),
        ),
    ]
