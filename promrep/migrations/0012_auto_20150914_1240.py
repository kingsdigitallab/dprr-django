# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('promrep', '0011_person_review_notes'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='postassertion',
            options={'ordering': ['id']},
        ),
    ]
