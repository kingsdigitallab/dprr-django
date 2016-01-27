# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('promrep', '0039_add_data_to_tribeassertion'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='person',
            name='tribe',
        ),
        migrations.RemoveField(
            model_name='person',
            name='tribe_uncertain',
        ),
    ]
