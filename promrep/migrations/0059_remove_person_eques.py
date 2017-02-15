# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('promrep', '0058_relationshiptype_order'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='person',
            name='eques',
        ),
        migrations.RemoveField(
            model_name='person',
            name='eques_notes',
        ),
        migrations.RemoveField(
            model_name='person',
            name='eques_uncertain',
        ),
    ]
