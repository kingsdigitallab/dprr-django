# -*- coding: utf-8 -*-


import django.utils.timezone
import model_utils.fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("promrep", "0048_statusassertionnote"),
    ]

    operations = [
        migrations.CreateModel(
            name="StatusAssertion",
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
                ("original_text", models.CharField(max_length=1024, blank=True)),
                (
                    "extra_info",
                    models.TextField(
                        help_text=b"Extra info about the status assertion", blank=True
                    ),
                ),
                (
                    "review_flag",
                    models.BooleanField(default=False, verbose_name=b"Review needed"),
                ),
                ("date_start", models.IntegerField(null=True, blank=True)),
                ("date_start_uncertain", models.BooleanField(default=False)),
                ("date_end", models.IntegerField(null=True, blank=True)),
                ("date_end_uncertain", models.BooleanField(default=False)),
                (
                    "date_display_text",
                    models.CharField(max_length=1024, null=True, blank=True),
                ),
                (
                    "date_source_text",
                    models.CharField(max_length=1024, null=True, blank=True),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        related_name="statusassertion_create",
                        verbose_name="author",
                        blank=True,
                        to=settings.AUTH_USER_MODEL,
                        null=True,
                    ),
                ),
                (
                    "date_secondary_source",
                    models.ForeignKey(
                        related_name="date_source",
                        blank=True,
                        to="promrep.SecondarySource",
                        null=True,
                    ),
                ),
                (
                    "notes",
                    models.ManyToManyField(
                        to="promrep.StatusAssertionNote", blank=True
                    ),
                ),
                ("person", models.ForeignKey(to="promrep.Person")),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="StatusAssertionProvince",
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
                    "uncertain",
                    models.BooleanField(default=False, verbose_name=b"Uncertain"),
                ),
                ("note", models.CharField(max_length=1024, blank=True)),
                (
                    "created_by",
                    models.ForeignKey(
                        related_name="statusassertionprovince_create",
                        verbose_name="author",
                        blank=True,
                        to=settings.AUTH_USER_MODEL,
                        null=True,
                    ),
                ),
                ("province", models.ForeignKey(to="promrep.Province")),
                ("status_assertion", models.ForeignKey(to="promrep.StatusAssertion")),
                (
                    "updated_by",
                    models.ForeignKey(
                        related_name="statusassertionprovince_update",
                        verbose_name="last updated by",
                        blank=True,
                        to=settings.AUTH_USER_MODEL,
                        null=True,
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="statusassertion",
            name="provinces",
            field=models.ManyToManyField(
                to="promrep.Province",
                through="promrep.StatusAssertionProvince",
                blank=True,
            ),
        ),
        migrations.AddField(
            model_name="statusassertion",
            name="secondary_source",
            field=models.ForeignKey(to="promrep.SecondarySource"),
        ),
        migrations.AddField(
            model_name="statusassertion",
            name="status",
            field=models.ForeignKey(to="promrep.StatusType"),
        ),
        migrations.AddField(
            model_name="statusassertion",
            name="updated_by",
            field=models.ForeignKey(
                related_name="statusassertion_update",
                verbose_name="last updated by",
                blank=True,
                to=settings.AUTH_USER_MODEL,
                null=True,
            ),
        ),
    ]
