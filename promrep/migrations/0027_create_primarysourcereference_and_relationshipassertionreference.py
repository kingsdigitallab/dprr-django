# -*- coding: utf-8 -*-


import django.utils.timezone
import model_utils.fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("promrep", "0026_remove_relationshipassertionprimarysource_model"),
    ]

    operations = [
        migrations.CreateModel(
            name="PrimarySourceReference",
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
                ("text", models.TextField(blank=True)),
                (
                    "created_by",
                    models.ForeignKey(
                        related_name="primarysourcereference_create",
                        verbose_name="author",
                        blank=True,
                        to=settings.AUTH_USER_MODEL,
                        null=True,
                    ),
                ),
                (
                    "note",
                    models.ForeignKey(
                        related_name="primary_source_references",
                        to="promrep.PrimarySource",
                        null=True,
                    ),
                ),
                (
                    "primary_source",
                    models.ForeignKey(
                        related_name="references", to="promrep.PrimarySource", null=True
                    ),
                ),
                (
                    "updated_by",
                    models.ForeignKey(
                        related_name="primarysourcereference_update",
                        verbose_name="last updated by",
                        blank=True,
                        to=settings.AUTH_USER_MODEL,
                        null=True,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="RelationshipAssertionReference",
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
                ("text", models.TextField(blank=True)),
                ("extra_info", models.TextField(max_length=1024, blank=True)),
                (
                    "created_by",
                    models.ForeignKey(
                        related_name="relationshipassertionreference_create",
                        verbose_name="author",
                        blank=True,
                        to=settings.AUTH_USER_MODEL,
                        null=True,
                    ),
                ),
                ("note_type", models.ForeignKey(default=1, to="promrep.NoteType")),
                (
                    "primary_source_references",
                    models.ManyToManyField(
                        to="promrep.PrimarySourceReference", blank=True
                    ),
                ),
                ("secondary_source", models.ForeignKey(to="promrep.SecondarySource")),
                (
                    "updated_by",
                    models.ForeignKey(
                        related_name="relationshipassertionreference_update",
                        verbose_name="last updated by",
                        blank=True,
                        to=settings.AUTH_USER_MODEL,
                        null=True,
                    ),
                ),
            ],
            options={
                "ordering": ["id"],
                "abstract": False,
            },
        ),
        migrations.AddField(
            model_name="personnote",
            name="primary_source_references",
            field=models.ManyToManyField(
                to="promrep.PrimarySourceReference", blank=True
            ),
        ),
        migrations.AddField(
            model_name="postassertionnote",
            name="primary_source_references",
            field=models.ManyToManyField(
                to="promrep.PrimarySourceReference", blank=True
            ),
        ),
    ]
