# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('promrep', '0018_add_notes_to_person'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='postassertion',
            options={'ordering': ['-date_end', '-date_start']},
        ),
        migrations.AlterField(
            model_name='postassertion',
            name='person',
            field=models.ForeignKey(related_name='post_assertions', to='promrep.Person'),
            preserve_default=True,
        ),
    ]