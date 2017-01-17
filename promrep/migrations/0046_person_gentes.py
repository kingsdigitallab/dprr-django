# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('promrep', '0045_remove_gens_fields_from_person'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='gentes',
            field=models.ManyToManyField(to='promrep.Gens', through='promrep.GensAssertion'),
        ),
    ]
