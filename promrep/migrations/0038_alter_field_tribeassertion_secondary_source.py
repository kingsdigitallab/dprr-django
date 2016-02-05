# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('promrep', '0037_add_model_tribeassertion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tribeassertion',
            name='secondary_source',
            field=models.ForeignKey(blank=True, to='promrep.SecondarySource', null=True),
        ),
    ]
