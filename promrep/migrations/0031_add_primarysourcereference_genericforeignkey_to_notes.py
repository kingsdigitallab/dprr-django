# -*- coding: utf-8 -*-


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("contenttypes", "0002_remove_content_type_name"),
        ("promrep", "0030_remove_primary_source_references_from_notes"),
    ]

    operations = [
        migrations.AddField(
            model_name="primarysourcereference",
            name="content_type",
            field=models.ForeignKey(
                verbose_name=b"primary source reference",
                blank=True,
                to="contenttypes.ContentType",
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="primarysourcereference",
            name="object_id",
            field=models.PositiveIntegerField(
                null=True, verbose_name=b"related object"
            ),
        ),
    ]
