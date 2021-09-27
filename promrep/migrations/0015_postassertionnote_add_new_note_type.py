# -*- coding: utf-8 -*-


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("promrep", "0014_rename_note_type"),
    ]

    operations = [
        migrations.AddField(
            model_name="postassertionnote",
            name="note_type",
            field=models.ForeignKey(
                default=1, to="promrep.NoteType",
                null=True, on_delete=models.SET_NULL
            ),
            preserve_default=True,

        ),
    ]
