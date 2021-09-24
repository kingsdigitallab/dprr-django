# -*- coding: utf-8 -*-


from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("promrep", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="postassertion",
            old_name="location",
            new_name="old_location",
        ),
    ]
