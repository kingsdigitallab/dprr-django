# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-08-01 14:44


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("wagtailbase", "0003_landingpage"),
    ]

    operations = [
        migrations.AddField(
            model_name="indexpage",
            name="icon",
            field=models.CharField(help_text="Icon", max_length=24, null=True),
        ),
    ]
