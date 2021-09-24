# -*- coding: utf-8 -*-


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("promrep", "0028_rename_field_notes_extra_info"),
    ]

    operations = [
        migrations.AddField(
            model_name="relationshipassertion",
            name="references",
            field=models.ManyToManyField(
                to="promrep.RelationshipAssertionReference", blank=True
            ),
        ),
    ]
