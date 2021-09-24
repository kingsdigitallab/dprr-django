# -*- coding: utf-8 -*-


from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("promrep", "0016_migrate_note_type_data"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="postassertionnote",
            name="old_note_type",
        ),
    ]
