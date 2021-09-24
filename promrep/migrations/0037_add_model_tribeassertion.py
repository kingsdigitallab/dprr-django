# -*- coding: utf-8 -*-


import django.utils.timezone
import model_utils.fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("promrep", "0036_remove_person_date_source_text"),
    ]

    operations = [
        migrations.CreateModel(
            name="TribeAssertion",
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
                (
                    "uncertain",
                    models.BooleanField(default=False, verbose_name=b"Uncertain"),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        related_name="tribeassertion_create",
                        verbose_name="author",
                        blank=True,
                        to=settings.AUTH_USER_MODEL,
                        null=True,
                    ),
                ),
                (
                    "notes",
                    models.ManyToManyField(to="promrep.PostAssertionNote", blank=True),
                ),
                ("person", models.ForeignKey(to="promrep.Person")),
                ("secondary_source", models.ForeignKey(to="promrep.SecondarySource")),
                (
                    "tribe",
                    models.ForeignKey(related_name="assertions", to="promrep.Tribe"),
                ),
                (
                    "updated_by",
                    models.ForeignKey(
                        related_name="tribeassertion_update",
                        verbose_name="last updated by",
                        blank=True,
                        to=settings.AUTH_USER_MODEL,
                        null=True,
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Tribe Assertions",
            },
        ),
    ]
