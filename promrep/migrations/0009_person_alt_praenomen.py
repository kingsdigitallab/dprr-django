# -*- coding: utf-8 -*-


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("promrep", "0008_person_other_names_uncertain"),
    ]

    operations = [
        migrations.AddField(
            model_name="person",
            name="alt_praenomen",
            field=models.ForeignKey(
                related_name="person_alt_praenomen_set",
                verbose_name="Uncertain Praenomen",
                blank=True,
                to="promrep.Praenomen",
                null=True,
                on_delete=models.SET_NULL
            ),
            preserve_default=True,
        ),
    ]
