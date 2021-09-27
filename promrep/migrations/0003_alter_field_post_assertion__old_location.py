# -*- coding: utf-8 -*-


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("promrep", "0002_rename_field_post_assertion__location"),
    ]

    operations = [
        migrations.AlterField(
            model_name="postassertion",
            name="old_location",
            field=models.ForeignKey(
                related_name="old_location",
                blank=True,
                to="promrep.Location",
                null=True,
                on_delete=models.SET_NULL,
            ),
            preserve_default=True,
        ),
    ]
