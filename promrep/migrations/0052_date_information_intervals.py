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
                default=b"S",
                max_length=1,
                verbose_name=b"Interval",
                choices=[(b"S", b"Single"), (b"B", b"Before"), (b"A", b"After")],
            ),
        ),
    ]
