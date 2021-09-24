# -*- coding: utf-8 -*-


from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("promrep", "0022_add_fields_to_primarysource"),
    ]

    operations = [
        migrations.RenameField(
            model_name="relationshipassertion",
            old_name="primary_source",
            new_name="primary_sources",
        ),
    ]
