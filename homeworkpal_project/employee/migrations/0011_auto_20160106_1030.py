# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('employee', '0010_achievement'),
    ]

    operations = [
        migrations.AddField(
            model_name='achievement',
            name='input_by',
            field=models.ForeignKey(default=1, to=settings.AUTH_USER_MODEL, related_name='achievement_inputs'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='companygroupemployeeassignment',
            name='role',
            field=models.CharField(default='MEMBER', max_length=6, choices=[('MEMBER', 'Member'), ('LEADER', 'Leader')]),
        ),
        migrations.AlterField(
            model_name='companygroup',
            name='parent_group',
            field=models.ForeignKey(null=True, verbose_name='children_groups', to='employee.CompanyGroup', blank=True),
        ),
    ]
