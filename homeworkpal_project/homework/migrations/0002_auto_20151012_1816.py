# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('homework', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('middle_name', models.CharField(blank=True, max_length=30, null=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='homework',
            name='teacher',
            field=models.ForeignKey(default=1, to='homework.Teacher'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='subject',
            name='teacher',
            field=models.ForeignKey(default=1, to='homework.Teacher'),
            preserve_default=False,
        ),
    ]
