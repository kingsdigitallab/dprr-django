# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import mptt
import mptt.managers
from django.db import migrations, models


def rebuild_province_mptt(apps, schema_editor):
    manager = mptt.managers.TreeManager()
    Province = apps.get_model("promrep", "Province")
    manager.model = Province
    mptt.register(Province, order_insertion_by=['name'])
    manager.contribute_to_class(Province, 'objects')
    manager.rebuild()


class Migration(migrations.Migration):

    dependencies = [
        ('promrep', '0053_convert_provinces_tree'),
    ]

    operations = [
        migrations.RunPython(rebuild_province_mptt,
                             migrations.RunPython.noop)
    ]
