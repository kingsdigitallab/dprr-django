# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('promrep', '0027_create_primarysourcereference_and_relationshipassertionreference'),
    ]

    operations = [
        migrations.RenameField('relationshipassertion', 'notes', 'extra_info'),
        migrations.AlterField(
            model_name='relationshipassertion',
            name='extra_info',
            field=models.TextField(help_text=b'Extra info about the relationship', blank=True),
        ),
    ]
