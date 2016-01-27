# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('promrep', '0044_add_data_to_gensassertion'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='person',
            name='gens',
        ),
        migrations.RemoveField(
            model_name='person',
            name='gens_uncertain',
        ),
    ]
