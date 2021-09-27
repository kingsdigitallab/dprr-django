# -*- coding: utf-8 -*-


import django.utils.timezone
import model_utils.fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("promrep", "0017_remove_postassertionnote_old_note_type"),
    ]

    operations = [
        migrations.CreateModel(
            name="PersonNote",
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
                        related_name="personnote_create",
                        verbose_name="author",
                        blank=True,
                        to=settings.AUTH_USER_MODEL,
                        null=True,
                        on_delete=models.SET_NULL
                    ),
                ),
                ("note_type", models.ForeignKey(
                    default=1, to="promrep.NoteType",
                    null=True, on_delete=models.SET_NULL
                )),
                ("secondary_source", models.ForeignKey(
                    to="promrep.SecondarySource",
                    null=True, on_delete=models.SET_NULL
                )),
                (
                    "updated_by",
                    models.ForeignKey(
                        related_name="personnote_update",
                        verbose_name="last updated by",
                        blank=True,
                        to=settings.AUTH_USER_MODEL,
                        null=True,
                        on_delete=models.SET_NULL
                    ),
                ),
            ],
            options={
                "ordering": ["id"],
                "abstract": False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name="person",
            name="notes",
            field=models.ManyToManyField(to="promrep.PersonNote", blank=True),
            preserve_default=True,
        ),
    ]
