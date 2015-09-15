# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('promrep', '0014_rename_note_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='postassertionnote',
            name='note_type',
            field=models.ForeignKey(default=1, to='promrep.NoteType'),
            preserve_default=True,
        ),
    ]
