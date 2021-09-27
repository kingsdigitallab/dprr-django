# -*- coding: utf-8 -*-


from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("promrep", "0023_rename_primarysources"),
    ]

    operations = [
        migrations.AlterField(
            model_name="relationshipassertionprimarysource",
            name="primary_source",
            field=models.ForeignKey(
                blank=True, to="promrep.PrimarySource",
                null=True, on_delete=models.SET_NULL
            ),
            preserve_default=True,
        ),
    ]
