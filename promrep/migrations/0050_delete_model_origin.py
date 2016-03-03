# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('promrep', '0049_create_statusassertion_statusassertionprovince'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='origin',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='origin',
            name='updated_by',
        ),
        migrations.RemoveField(
            model_name='person',
            name='origin',
        ),
        migrations.DeleteModel(
            name='Origin',
        ),
    ]
