# -*- coding: utf-8 -*-


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("promrep", "0054_rebuild_provinces_tree"),
    ]

    operations = [
        migrations.AddField(
            model_name="person",
            name="highest_office",
            field=models.CharField(max_length=1024, null=True, blank=True),
        ),
        migrations.AddField(
            model_name="person",
            name="highest_office_edited",
            field=models.BooleanField(default=False),
        ),
    ]
