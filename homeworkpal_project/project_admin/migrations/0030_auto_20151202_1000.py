# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_admin', '0029_auto_20151118_1445'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectmember',
            name='role',
            field=models.CharField(max_length=15, choices=[('MEMBER', 'Team Member'), ('LEADER', 'Team Leader'), ('PRODUCT_OWNER', 'Product Owner')]),
        ),
    ]
