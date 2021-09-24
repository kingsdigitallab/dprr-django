# -*- coding: utf-8 -*-


from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("promrep", "0003_alter_field_post_assertion__old_location"),
    ]

    operations = [
        migrations.RenameModel("Location", "Province"),
        migrations.RemoveField("Province", "location_type"),
        migrations.AlterModelOptions(
            name="province",
            options={"verbose_name": "Province", "verbose_name_plural": "Provinces"},
        ),
        migrations.AlterField(
            model_name="province",
            name="created_by",
            field=models.ForeignKey(
                related_name="province_create",
                verbose_name="author",
                blank=True,
                to=settings.AUTH_USER_MODEL,
                null=True,
            ),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name="province",
            name="updated_by",
            field=models.ForeignKey(
                related_name="province_update",
                verbose_name="last updated by",
                blank=True,
                to=settings.AUTH_USER_MODEL,
                null=True,
            ),
            preserve_default=True,
        ),
    ]
