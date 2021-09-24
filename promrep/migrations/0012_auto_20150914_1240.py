# -*- coding: utf-8 -*-


from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("promrep", "0011_person_review_notes"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="postassertion",
            options={"ordering": ["id"]},
        ),
    ]
