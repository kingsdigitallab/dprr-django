# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('promrep', '0034_dateinformation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dateinformation',
            name='notes',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='dateinformation',
            name='source_text',
            field=models.TextField(blank=True),
        ),
    ]
