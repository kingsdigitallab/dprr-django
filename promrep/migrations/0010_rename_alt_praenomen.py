# -*- coding: utf-8 -*-


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("promrep", "0009_person_alt_praenomen"),
    ]

    operations = [
        migrations.AlterField(
            model_name="person",
            name="alt_praenomen",
            field=models.ForeignKey(
                related_name="person_alt_praenomen_set",
                verbose_name=b"Alternative Praenomen",
                blank=True,
                to="promrep.Praenomen",
                null=True,
                on_delete=models.SET_NULL,
            ),
            preserve_default=True,
        ),
    ]
