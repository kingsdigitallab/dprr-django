# -*- coding: utf-8 -*-


from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("promrep", "0025_remove_primarysource_from_relationshipassertion"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="relationshipassertionprimarysource",
            name="created_by",
        ),
        migrations.RemoveField(
            model_name="relationshipassertionprimarysource",
            name="primary_source",
        ),
        migrations.RemoveField(
            model_name="relationshipassertionprimarysource",
            name="relationship_assertion",
        ),
        migrations.RemoveField(
            model_name="relationshipassertionprimarysource",
            name="updated_by",
        ),
        migrations.DeleteModel(
            name="RelationshipAssertionPrimarySource",
        ),
    ]
