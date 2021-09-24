# -*- coding: utf-8 -*-


from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("promrep", "0044_add_data_to_gensassertion"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="person",
            name="gens",
        ),
        migrations.RemoveField(
            model_name="person",
            name="gens_uncertain",
        ),
    ]
