# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('promrep', '0024_alter_primary_source_relationshipassertionprimarysource'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='relationshipassertion',
            options={'ordering': ['relationship_number', 'id']},
        ),
        migrations.RemoveField(
            model_name='relationshipassertion',
            name='primary_sources',
        ),
    ]
