# -*- coding: utf-8 -*-


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("promrep", "0032_auto_20160126_1021"),
    ]

    operations = [
        migrations.AlterField(
            model_name="postassertion",
            name="provinces",
            field=models.ManyToManyField(
                to="promrep.Province",
                through="promrep.PostAssertionProvince",
                blank=True,
            ),
        ),
    ]
