# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('promrep', '0005_create_postassertionprovince'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='postassertion',
            name='old_location',
        ),
    ]
