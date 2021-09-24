# -*- coding: utf-8 -*-


from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("promrep", "0005_create_postassertionprovince"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="postassertion",
            name="old_location",
        ),
    ]
