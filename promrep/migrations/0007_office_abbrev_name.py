# -*- coding: utf-8 -*-


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("promrep", "0006_remove_postassertion_old_location"),
    ]

    operations = [
        migrations.AddField(
            model_name="office",
            name="abbrev_name",
            field=models.CharField(max_length=128, blank=True),
            preserve_default=True,
        ),
    ]
