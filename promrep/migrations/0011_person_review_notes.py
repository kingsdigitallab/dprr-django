# -*- coding: utf-8 -*-


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("promrep", "0010_rename_alt_praenomen"),
    ]

    operations = [
        migrations.AddField(
            model_name="person",
            name="review_notes",
            field=models.TextField(blank=True),
            preserve_default=True,
        ),
    ]
