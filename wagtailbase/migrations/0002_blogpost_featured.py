# -*- coding: utf-8 -*-


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("wagtailbase", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="blogpost",
            name="featured",
            field=models.BooleanField(default=False, help_text="Feature this post"),
            preserve_default=True,
        ),
    ]
