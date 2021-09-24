# -*- coding: utf-8 -*-


from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("promrep", "0058_relationshiptype_order"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="person",
            name="eques",
        ),
        migrations.RemoveField(
            model_name="person",
            name="eques_notes",
        ),
        migrations.RemoveField(
            model_name="person",
            name="eques_uncertain",
        ),
    ]
