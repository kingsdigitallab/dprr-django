# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('promrep', '0002_rename_field_post_assertion__location'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postassertion',
            name='old_location',
            field=models.ForeignKey(related_name='old_location', blank=True, to='promrep.Location', null=True),
            preserve_default=True,
        ),
    ]
