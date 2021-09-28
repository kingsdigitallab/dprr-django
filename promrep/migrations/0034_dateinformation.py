# -*- coding: utf-8 -*-


import django.utils.timezone
import model_utils.fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("promrep", "0033_auto_20160126_1023"),
    ]

    operations = [
        migrations.CreateModel(
            name="DateInformation",
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
                    "date_interval",
                    models.CharField(
                        default="A",
                        max_length=1,
                        verbose_name="Interval",
                        choices=[
                            ("A", "Attestation"),
                            ("F", "First"),
                            ("L", "Last"),
                        ],
                    ),
                ),
                ("uncertain", models.BooleanField(default=False)),
                ("value", models.IntegerField()),
                ("source_text", models.TextField()),
                ("notes", models.TextField()),
                (
                    "created_by",
                    models.ForeignKey(
                        related_name="dateinformation_create",
                        verbose_name="author",
                        blank=True,
                        to=settings.AUTH_USER_MODEL,
                        null=True,
                        on_delete=models.SET_NULL
                    ),
                ),
                (
                    "date_type",
                    models.ForeignKey(
                        related_name="person_date",
                        verbose_name="Type",
                        to="promrep.DateType",
                        null=True, on_delete=models.SET_NULL
                    ),
                ),
                ("person", models.ForeignKey(
                    to="promrep.Person",
                    null=True, on_delete=models.SET_NULL
                )),
                (
                    "secondary_source",
                    models.ForeignKey(
                        blank=True, to="promrep.SecondarySource",
                        null=True, on_delete=models.SET_NULL
                    ),
                ),
                (
                    "updated_by",
                    models.ForeignKey(
                        related_name="dateinformation_update",
                        verbose_name="last updated by",
                        blank=True,
                        to=settings.AUTH_USER_MODEL,
                        null=True, on_delete=models.SET_NULL
                    ),
                ),
            ],
            options={
                "verbose_name": "Date",
            },
        ),
    ]
