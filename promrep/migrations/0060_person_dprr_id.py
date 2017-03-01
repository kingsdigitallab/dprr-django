# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('promrep', '0059_remove_person_eques'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='dprr_id',
            field=models.CharField(max_length=16, null=True, blank=True, unique=True),
        ),
    ]
