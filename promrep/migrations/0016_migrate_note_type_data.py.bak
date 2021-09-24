# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def populate_new_note_types(apps, schema_editor):
    """Populates the new note types"""
    postassertion_note_model = apps.get_model('promrep', 'PostAssertionNote')

    for pan in postassertion_note_model.objects.all():
        if pan.old_note_type:
            # the new note types need to be incremented by one
            pan.note_type_id = pan.old_note_type + 1
            pan.save()


def populate_old_note_types(apps, schema_editor):
    """Populates the new note types"""
    postassertion_note_model = apps.get_model('promrep', 'PostAssertionNote')

    for pan in postassertion_note_model.objects.all():
        if pan.note_type:
            # the old note types need to be decremented by one
            pan.old_note_type = pan.note_type_id - 1
            pan.save()


class Migration(migrations.Migration):

    dependencies = [
        ('promrep', '0015_postassertionnote_add_new_note_type'),
    ]

    operations = [
        migrations.RunPython(
            populate_new_note_types, reverse_code=populate_old_note_types),

    ]
