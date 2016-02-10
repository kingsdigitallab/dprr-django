# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('promrep', '0041_person_tribes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tribeassertion',
            name='notes',
        ),
        migrations.AddField(
            model_name='tribeassertion',
            name='notes',
            field=models.TextField(blank=True),
        ),
    ]
