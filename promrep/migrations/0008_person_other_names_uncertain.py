# -*- coding: utf-8 -*-


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("promrep", "0007_office_abbrev_name"),
    ]

    operations = [
        migrations.AddField(
            model_name="person",
            name="other_names_uncertain",
            field=models.BooleanField(
                default=False, verbose_name="Uncertain Other Names"
            ),
            preserve_default=True,
        ),
    ]
