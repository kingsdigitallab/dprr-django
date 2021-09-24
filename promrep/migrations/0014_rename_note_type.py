# -*- coding: utf-8 -*-


from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("promrep", "0013_add_notetype"),
    ]

    operations = [
        migrations.RenameField(
            model_name="postassertionnote",
            old_name="note_type",
            new_name="old_note_type",
        ),
    ]
