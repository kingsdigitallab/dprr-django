# -*- coding: utf-8 -*-


from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "promrep",
            "0027_create_primarysourcereference_and" "_relationshipassertionreference",
        ),
    ]

    operations = [
        migrations.RenameField("relationshipassertion", "notes", "extra_info"),
        migrations.AlterField(
            model_name="relationshipassertion",
            name="extra_info",
            field=models.TextField(
                help_text=b"Extra info about the relationship", blank=True
            ),
        ),
    ]
