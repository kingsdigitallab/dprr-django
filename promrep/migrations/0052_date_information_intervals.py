# -*- coding: utf-8 -*-


from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("promrep", "0051_person_origin"),
    ]

    operations = [
        migrations.AlterField(
            model_name="dateinformation",
            name="date_interval",
            field=models.CharField(
                default="S",
                max_length=1,
                verbose_name="Interval",
                choices=[("S", "Single"), ("B", "Before"), ("A", "After")],
            ),
        ),
    ]
