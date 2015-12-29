# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import model_utils.fields
import django.core.validators
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('project_admin', '0011_auto_20151104_2159'),
        ('employee', '0006_auto_20151104_2159'),
    ]

    operations = [
        migrations.CreateModel(
            name='MaximoTicket',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(verbose_name='created', editable=False, default=django.utils.timezone.now)),
                ('modified', model_utils.fields.AutoLastModifiedField(verbose_name='modified', editable=False, default=django.utils.timezone.now)),
                ('ticket_type', models.CharField(default='SR', max_length=2, choices=[('SR', 'Service Request'), ('WO', 'Work Order')])),
                ('number', models.CharField(validators=[django.core.validators.RegexValidator(regex='\\d{6}')], max_length=7)),
                ('name', models.CharField(max_length=120)),
                ('is_open', models.BooleanField(default=True)),
                ('project', models.ForeignKey(related_name='maximo_tickets', blank=True, null=True, to='project_admin.Project')),
            ],
            options={
                'ordering': ('number',),
            },
        ),
        migrations.CreateModel(
            name='MaximoTimeRegister',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(verbose_name='created', editable=False, default=django.utils.timezone.now)),
                ('modified', model_utils.fields.AutoLastModifiedField(verbose_name='modified', editable=False, default=django.utils.timezone.now)),
                ('date', models.DateField()),
                ('regular_hours', models.DecimalField(max_digits=5, decimal_places=2)),
                ('description', models.TextField(null=True, blank=True)),
                ('employee', models.ForeignKey(related_name='maximo_time_registers', to='employee.Employee')),
                ('project', models.ForeignKey(related_name='maximo_time_registers', blank=True, null=True, to='project_admin.Project')),
                ('ticket', models.ForeignKey(related_name='time_registers', to='maximo.MaximoTicket')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterUniqueTogether(
            name='maximoticket',
            unique_together=set([('ticket_type', 'number')]),
        ),
    ]
