# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('promrep', '0008_person_other_names_uncertain'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='alt_praenomen',
            field=models.ForeignKey(related_name='person_alt_praenomen_set', verbose_name=b'Uncertain Praenomen', blank=True, to='promrep.Praenomen', null=True),
            preserve_default=True,
        ),
    ]