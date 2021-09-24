# -*- coding: utf-8 -*-


import mptt.fields
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("promrep", "0052_date_information_intervals"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="province",
            options={
                "ordering": ["tree_id", "lft", "name"],
                "verbose_name": "Province",
                "verbose_name_plural": "Provinces",
            },
        ),
        migrations.AddField(
            model_name="province",
            name="level",
            field=models.PositiveIntegerField(default=0, editable=False, db_index=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="province",
            name="lft",
            field=models.PositiveIntegerField(default=0, editable=False, db_index=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="province",
            name="parent",
            field=mptt.fields.TreeForeignKey(
                related_name="children", blank=True, to="promrep.Province", null=True
            ),
        ),
        migrations.AddField(
            model_name="province",
            name="rght",
            field=models.PositiveIntegerField(default=0, editable=False, db_index=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="province",
            name="tree_id",
            field=models.PositiveIntegerField(default=0, editable=False, db_index=True),
            preserve_default=False,
        ),
    ]
