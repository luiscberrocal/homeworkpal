# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interviews', '0004_auto_20151126_1116'),
    ]

    operations = [
        migrations.AddField(
            model_name='contactattempt',
            name='candidate_certificate',
            field=models.ForeignKey(related_name='attempts_to_contact', default=1, to='interviews.CandidateInCertificate'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='certificateresult',
            name='observations',
            field=models.TextField(blank=True),
        ),
    ]
