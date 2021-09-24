# -*- coding: utf-8 -*-


from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("promrep", "0024_alter_primary_source_relationshipassertionprimarysource"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="relationshipassertion",
            options={"ordering": ["relationship_number", "id"]},
        ),
        migrations.RemoveField(
            model_name="relationshipassertion",
            name="primary_sources",
        ),
    ]
