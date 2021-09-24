# -*- coding: utf-8 -*-


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("promrep", "0057_add_relationship_types"),
    ]

    operations = [
        migrations.AddField(
            model_name="relationshiptype",
            name="order",
            field=models.PositiveSmallIntegerField(default=0),
        ),
    ]
