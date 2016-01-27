# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('promrep', '0040_remove_tribe_fields_from_person'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='tribes',
            field=models.ManyToManyField(to='promrep.Tribe', through='promrep.TribeAssertion'),
        ),
    ]
