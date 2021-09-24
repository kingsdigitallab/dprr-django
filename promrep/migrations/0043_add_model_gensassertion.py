# -*- coding: utf-8 -*-


import django.utils.timezone
import model_utils.fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("promrep", "0042_alter_field_tribeassertion_notes"),
    ]

    operations = [
        migrations.CreateModel(
            name="GensAssertion",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                (
                    "created",
                    model_utils.fields.AutoCreatedField(
                        default=django.utils.timezone.now,
                        verbose_name="created",
                        editable=False,
                    ),
                ),
                (
                    "modified",
                    model_utils.fields.AutoLastModifiedField(
                        default=django.utils.timezone.now,
                        verbose_name="modified",
                        editable=False,
                    ),
                ),
                ("uncertain", models.BooleanField(default=False)),
                ("notes", models.TextField(blank=True)),
                (
                    "created_by",
                    models.ForeignKey(
                        related_name="gensassertion_create",
                        verbose_name="author",
                        blank=True,
                        to=settings.AUTH_USER_MODEL,
                        null=True,
                    ),
                ),
                (
                    "gens",
                    models.ForeignKey(related_name="assertions", to="promrep.Gens"),
                ),
                ("person", models.ForeignKey(to="promrep.Person")),
                (
                    "secondary_source",
                    models.ForeignKey(
                        blank=True, to="promrep.SecondarySource", null=True
                    ),
                ),
                (
                    "updated_by",
                    models.ForeignKey(
                        related_name="gensassertion_update",
                        verbose_name="last updated by",
                        blank=True,
                        to=settings.AUTH_USER_MODEL,
                        null=True,
                    ),
                ),
            ],
            options={
                "verbose_name": "Gens",
                "verbose_name_plural": "Gentes",
            },
        ),
        migrations.AlterModelOptions(
            name="tribeassertion",
            options={"verbose_name": "Tribe"},
        ),
    ]
