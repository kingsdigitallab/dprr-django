# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('promrep', '0016_migrate_note_type_data'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='postassertionnote',
            name='old_note_type',
        ),
    ]
