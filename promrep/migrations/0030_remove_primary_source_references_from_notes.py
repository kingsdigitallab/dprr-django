# -*- coding: utf-8 -*-


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("promrep", "0029_relationshipassertion_references"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="personnote",
            name="primary_source_references",
        ),
        migrations.RemoveField(
            model_name="postassertionnote",
            name="primary_source_references",
        ),
        migrations.RemoveField(
            model_name="primarysourcereference",
            name="note",
        ),
        migrations.RemoveField(
            model_name="relationshipassertionreference",
            name="primary_source_references",
        ),
        migrations.AlterField(
            model_name="primarysourcereference",
            name="primary_source",
            field=models.ForeignKey(
                to="promrep.PrimarySource",
                null=True, on_delete=models.SET_NULL
            ),
        ),
    ]
