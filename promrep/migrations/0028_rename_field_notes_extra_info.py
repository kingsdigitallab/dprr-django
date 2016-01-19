# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('promrep', '0027_create_primarysourcereference_and_relationshipassertionreference'),
    ]

    operations = [
        migrations.RenameField('relationshipassertion', 'notes', 'extra_info'),
    ]
