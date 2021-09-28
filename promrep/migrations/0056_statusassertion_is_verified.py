# -*- coding: utf-8 -*-


from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("promrep", "0055_add_highest_office_field"),
    ]

    operations = [
        migrations.AddField(
            model_name="statusassertion",
            name="is_verified",
            field=models.BooleanField(default=False, verbose_name="Editor Verified"),
        ),
    ]
