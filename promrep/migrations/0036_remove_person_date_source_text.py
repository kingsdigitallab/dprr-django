# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('promrep', '0035_auto_20160126_1132'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='person',
            name='date_source_text',
        ),
    ]
