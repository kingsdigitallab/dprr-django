# -*- coding: utf-8 -*-


from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("promrep", "0035_auto_20160126_1132"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="person",
            name="date_source_text",
        ),
    ]
