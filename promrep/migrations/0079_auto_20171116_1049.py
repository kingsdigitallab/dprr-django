# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-11-16 10:49


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("promrep", "0078_auto_20170821_1027"),
    ]

    operations = [
        migrations.AlterField(
            model_name="relationshiptype",
            name="description",
            field=models.CharField(blank=True, max_length=1024, null=True),
        ),
    ]
