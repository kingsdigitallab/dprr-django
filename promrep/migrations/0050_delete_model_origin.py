# -*- coding: utf-8 -*-


from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("promrep", "0049_create_statusassertion_statusassertionprovince"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="origin",
            name="created_by",
        ),
        migrations.RemoveField(
            model_name="origin",
            name="updated_by",
        ),
        migrations.RemoveField(
            model_name="person",
            name="origin",
        ),
        migrations.DeleteModel(
            name="Origin",
        ),
    ]
