# -*- coding: utf-8 -*-


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("promrep", "0021_create_relationshipassertion"),
    ]

    operations = [
        migrations.AddField(
            model_name="primarysource",
            name="abbrev_name",
            field=models.CharField(unique=True, max_length=256, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name="primarysource",
            name="biblio",
            field=models.CharField(unique=True, max_length=512, blank=True),
            preserve_default=True,
        ),
    ]
