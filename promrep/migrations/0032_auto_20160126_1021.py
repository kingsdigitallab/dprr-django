# -*- coding: utf-8 -*-


from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("promrep", "0031_add_primarysourcereference_genericforeignkey_to_notes"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="person",
            name="date_first",
        ),
        migrations.RemoveField(
            model_name="person",
            name="date_first_type",
        ),
        migrations.RemoveField(
            model_name="person",
            name="date_last",
        ),
        migrations.RemoveField(
            model_name="person",
            name="date_last_type",
        ),
        migrations.RemoveField(
            model_name="person",
            name="date_secondary_source",
        ),
    ]
