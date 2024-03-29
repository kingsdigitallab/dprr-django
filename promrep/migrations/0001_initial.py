# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import django.utils.timezone
import model_utils.fields
import mptt.fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="DateType",
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
                ("name", models.CharField(unique=True, max_length=256)),
                ("description", models.CharField(max_length=1024, blank=True)),
                (
                    "created_by",
                    models.ForeignKey(
                        related_name="datetype_create",
                        verbose_name="author",
                        blank=True,
                        to=settings.AUTH_USER_MODEL,
                        null=True,
                        on_delete=models.SET_NULL,
                    ),
                ),
                (
                    "updated_by",
                    models.ForeignKey(
                        related_name="datetype_update",
                        verbose_name="last updated by",
                        blank=True,
                        to=settings.AUTH_USER_MODEL,
                        null=True,
                        on_delete=models.SET_NULL,
                    ),
                ),
            ],
            options={
                "ordering": ["name"],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name="Gens",
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
                ("name", models.CharField(unique=True, max_length=128)),
                ("extra_info", models.CharField(max_length=1024, blank=True)),
                (
                    "created_by",
                    models.ForeignKey(
                        related_name="gens_create",
                        verbose_name="author",
                        blank=True,
                        to=settings.AUTH_USER_MODEL,
                        null=True,
                        on_delete=models.SET_NULL,
                    ),
                ),
                (
                    "updated_by",
                    models.ForeignKey(
                        related_name="gens_update",
                        verbose_name="last updated by",
                        blank=True,
                        to=settings.AUTH_USER_MODEL,
                        null=True,
                        on_delete=models.SET_NULL,
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Gens",
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name="Group",
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
                ("display_text", models.CharField(max_length=1024, blank=True)),
                ("notes", models.TextField(blank=True)),
                ("date_year", models.IntegerField(null=True, blank=True)),
                ("date_info", models.CharField(max_length=1024, null=True, blank=True)),
                (
                    "created_by",
                    models.ForeignKey(
                        related_name="group_create",
                        verbose_name="author",
                        blank=True,
                        to=settings.AUTH_USER_MODEL,
                        null=True,
                        on_delete=models.SET_NULL,
                    ),
                ),
            ],
            options={
                "ordering": ["id"],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name="Location",
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
                ("name", models.CharField(unique=True, max_length=256)),
                ("description", models.CharField(max_length=1024, blank=True)),
                (
                    "location_type",
                    models.SmallIntegerField(
                        default=0, choices=[(0, "place"), (1, "province")]
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        related_name="location_create",
                        verbose_name="author",
                        blank=True,
                        to=settings.AUTH_USER_MODEL,
                        null=True,
                        on_delete=models.SET_NULL,
                    ),
                ),
                (
                    "updated_by",
                    models.ForeignKey(
                        related_name="location_update",
                        verbose_name="last updated by",
                        blank=True,
                        to=settings.AUTH_USER_MODEL,
                        null=True,
                        on_delete=models.SET_NULL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Places",
                "verbose_name_plural": "Place List",
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name="Office",
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
                ("name", models.CharField(unique=True, max_length=256)),
                ("description", models.CharField(max_length=1024, blank=True)),
                ("lft", models.PositiveIntegerField(editable=False, db_index=True)),
                ("rght", models.PositiveIntegerField(editable=False, db_index=True)),
                ("tree_id", models.PositiveIntegerField(editable=False, db_index=True)),
                ("level", models.PositiveIntegerField(editable=False, db_index=True)),
                (
                    "created_by",
                    models.ForeignKey(
                        related_name="office_create",
                        verbose_name="author",
                        blank=True,
                        to=settings.AUTH_USER_MODEL,
                        null=True,
                        on_delete=models.SET_NULL,
                    ),
                ),
                (
                    "parent",
                    mptt.fields.TreeForeignKey(
                        related_name="children",
                        blank=True,
                        to="promrep.Office",
                        null=True,
                        on_delete=models.SET_NULL,
                    ),
                ),
                (
                    "updated_by",
                    models.ForeignKey(
                        related_name="office_update",
                        verbose_name="last updated by",
                        blank=True,
                        to=settings.AUTH_USER_MODEL,
                        null=True,
                        on_delete=models.SET_NULL,
                    ),
                ),
            ],
            options={
                "ordering": ["tree_id", "lft", "name"],
                "verbose_name": "Office",
                "verbose_name_plural": "Office",
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name="Origin",
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
                ("name", models.CharField(unique=True, max_length=128)),
                ("extra_info", models.CharField(max_length=1024, blank=True)),
                (
                    "created_by",
                    models.ForeignKey(
                        related_name="origin_create",
                        verbose_name="author",
                        blank=True,
                        to=settings.AUTH_USER_MODEL,
                        null=True,
                        on_delete=models.SET_NULL,
                    ),
                ),
                (
                    "updated_by",
                    models.ForeignKey(
                        related_name="origin_update",
                        verbose_name="last updated by",
                        blank=True,
                        to=settings.AUTH_USER_MODEL,
                        null=True,
                        on_delete=models.SET_NULL,
                    ),
                ),
            ],
            options={},
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name="Person",
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
                    "praenomen_uncertain",
                    models.BooleanField(
                        default=False, verbose_name="Uncertain Praenomen"
                    ),
                ),
                ("nomen", models.CharField(max_length=128, blank=True)),
                (
                    "nomen_uncertain",
                    models.BooleanField(default=False, verbose_name="Uncertain Nomen"),
                ),
                ("cognomen", models.CharField(max_length=64, blank=True)),
                (
                    "cognomen_uncertain",
                    models.BooleanField(
                        default=False, verbose_name="Uncertain Cognomen"
                    ),
                ),
                ("other_names", models.CharField(max_length=128, blank=True)),
                ("filiation", models.CharField(max_length=256, blank=True)),
                (
                    "filiation_uncertain",
                    models.BooleanField(
                        default=False, verbose_name="Uncertain Filiation"
                    ),
                ),
                (
                    "gens_uncertain",
                    models.BooleanField(default=False, verbose_name="Uncertain Gens"),
                ),
                (
                    "tribe_uncertain",
                    models.BooleanField(default=False, verbose_name="Uncertain Tribe"),
                ),
                (
                    "re_number",
                    models.CharField(
                        help_text="RE number",
                        max_length=32,
                        verbose_name="RE Number",
                        blank=True,
                    ),
                ),
                (
                    "re_number_old",
                    models.CharField(
                        help_text="RE number before revising",
                        max_length=32,
                        verbose_name="RE (old)",
                        blank=True,
                    ),
                ),
                (
                    "patrician",
                    models.NullBooleanField(default=None, verbose_name="Patrician"),
                ),
                (
                    "patrician_uncertain",
                    models.BooleanField(
                        default=False, verbose_name="Uncertain Patrician"
                    ),
                ),
                ("patrician_notes", models.TextField(blank=True)),
                ("novus", models.NullBooleanField(default=None)),
                ("novus_uncertain", models.NullBooleanField(default=False)),
                ("novus_notes", models.TextField(blank=True)),
                ("eques", models.NullBooleanField(default=None)),
                ("eques_uncertain", models.BooleanField(default=False)),
                ("eques_notes", models.TextField(blank=True)),
                ("nobilis", models.NullBooleanField(default=None)),
                ("nobilis_uncertain", models.BooleanField(default=False)),
                ("nobilis_notes", models.TextField(blank=True)),
                (
                    "extra_info",
                    models.TextField(
                        help_text="Extra info about the person.", blank=True
                    ),
                ),
                (
                    "date_display_text",
                    models.CharField(max_length=1024, null=True, blank=True),
                ),
                (
                    "date_source_text",
                    models.CharField(max_length=1024, null=True, blank=True),
                ),
                ("date_first", models.IntegerField(null=True, blank=True)),
                ("date_last", models.IntegerField(null=True, blank=True)),
                ("era_from", models.IntegerField(null=True, blank=True)),
                ("era_to", models.IntegerField(null=True, blank=True)),
                (
                    "review_flag",
                    models.BooleanField(
                        default=False,
                        help_text="Person needs manual revision.",
                        verbose_name="Review needed",
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        related_name="person_create",
                        verbose_name="author",
                        blank=True,
                        to=settings.AUTH_USER_MODEL,
                        null=True,
                        on_delete=models.SET_NULL,
                    ),
                ),
                (
                    "date_first_type",
                    models.ForeignKey(
                        related_name="person_first",
                        blank=True,
                        to="promrep.DateType",
                        null=True,
                        on_delete=models.SET_NULL,
                    ),
                ),
                (
                    "date_last_type",
                    models.ForeignKey(
                        related_name="person_last",
                        blank=True,
                        to="promrep.DateType",
                        null=True,
                        on_delete=models.SET_NULL,
                    ),
                ),
            ],
            options={
                "ordering": ["id"],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name="PostAssertion",
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
                ("original_text", models.CharField(max_length=1024, blank=True)),
                ("office_xref", models.CharField(max_length=1024, blank=True)),
                (
                    "uncertain",
                    models.BooleanField(default=False, verbose_name="Uncertain"),
                ),
                ("position", models.PositiveSmallIntegerField(default=0)),
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
                    "review_flag",
                    models.BooleanField(
                        default=False,
                        help_text="Manual revision needed.",
                        verbose_name="Review needed",
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        related_name="postassertion_create",
                        verbose_name="author",
                        blank=True,
                        to=settings.AUTH_USER_MODEL,
                        null=True,
                        on_delete=models.SET_NULL,
                    ),
                ),
            ],
            options={
                "ordering": ["position", "id"],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name="PostAssertionNote",
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
                    "note_type",
                    models.IntegerField(
                        default=0,
                        choices=[
                            (0, "Reference"),
                            (1, "Footnote"),
                            (2, "Reference (Office)"),
                            (3, "Footnote (Office)"),
                        ],
                    ),
                ),
                ("text", models.TextField(blank=True)),
                ("extra_info", models.TextField(max_length=1024, blank=True)),
                (
                    "created_by",
                    models.ForeignKey(
                        related_name="postassertionnote_create",
                        verbose_name="author",
                        blank=True,
                        to=settings.AUTH_USER_MODEL,
                        null=True,
                        on_delete=models.SET_NULL,
                    ),
                ),
            ],
            options={
                "ordering": ["id"],
                "abstract": False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name="Praenomen",
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
                ("abbrev", models.CharField(unique=True, max_length=32)),
                ("name", models.CharField(unique=True, max_length=128)),
                (
                    "created_by",
                    models.ForeignKey(
                        related_name="praenomen_create",
                        verbose_name="author",
                        blank=True,
                        to=settings.AUTH_USER_MODEL,
                        null=True,
                        on_delete=models.SET_NULL,
                    ),
                ),
                (
                    "updated_by",
                    models.ForeignKey(
                        related_name="praenomen_update",
                        verbose_name="last updated by",
                        blank=True,
                        to=settings.AUTH_USER_MODEL,
                        null=True,
                        on_delete=models.SET_NULL,
                    ),
                ),
            ],
            options={
                "ordering": ["name"],
                "verbose_name_plural": "Praenomina",
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name="PrimarySource",
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
                ("name", models.CharField(unique=True, max_length=256)),
            ],
            options={},
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name="Relationship",
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
                ("name", models.CharField(unique=True, max_length=256)),
                ("description", models.CharField(max_length=1024, blank=True)),
                (
                    "created_by",
                    models.ForeignKey(
                        related_name="relationship_create",
                        verbose_name="author",
                        blank=True,
                        to=settings.AUTH_USER_MODEL,
                        null=True,
                        on_delete=models.SET_NULL,
                    ),
                ),
                (
                    "updated_by",
                    models.ForeignKey(
                        related_name="relationship_update",
                        verbose_name="last updated by",
                        blank=True,
                        to=settings.AUTH_USER_MODEL,
                        null=True,
                        on_delete=models.SET_NULL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name="RoleType",
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
                ("name", models.CharField(unique=True, max_length=128)),
                ("description", models.CharField(max_length=1024, blank=True)),
            ],
            options={
                "abstract": False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name="SecondarySource",
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
                ("name", models.CharField(unique=True, max_length=256)),
                (
                    "abbrev_name",
                    models.CharField(unique=True, max_length=256, blank=True),
                ),
                ("biblio", models.CharField(unique=True, max_length=512, blank=True)),
                (
                    "created_by",
                    models.ForeignKey(
                        related_name="secondarysource_create",
                        verbose_name="author",
                        blank=True,
                        to=settings.AUTH_USER_MODEL,
                        null=True,
                        on_delete=models.SET_NULL,
                    ),
                ),
                (
                    "updated_by",
                    models.ForeignKey(
                        related_name="secondarysource_update",
                        verbose_name="last updated by",
                        blank=True,
                        to=settings.AUTH_USER_MODEL,
                        null=True,
                        on_delete=models.SET_NULL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name="Sex",
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
                ("name", models.CharField(unique=True, max_length=32)),
            ],
            options={},
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name="Tribe",
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
                ("abbrev", models.CharField(unique=True, max_length=32)),
                ("name", models.CharField(max_length=128)),
                ("extra_info", models.CharField(max_length=1024, blank=True)),
                (
                    "created_by",
                    models.ForeignKey(
                        related_name="tribe_create",
                        verbose_name="author",
                        blank=True,
                        to=settings.AUTH_USER_MODEL,
                        null=True,
                        on_delete=models.SET_NULL,
                    ),
                ),
                (
                    "updated_by",
                    models.ForeignKey(
                        related_name="tribe_update",
                        verbose_name="last updated by",
                        blank=True,
                        to=settings.AUTH_USER_MODEL,
                        null=True,
                        on_delete=models.SET_NULL,
                    ),
                ),
            ],
            options={
                "ordering": ["id"],
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name="postassertionnote",
            name="secondary_source",
            field=models.ForeignKey(
                to="promrep.SecondarySource", null=True, on_delete=models.SET_NULL
            ),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name="postassertionnote",
            name="updated_by",
            field=models.ForeignKey(
                related_name="postassertionnote_update",
                verbose_name="last updated by",
                blank=True,
                to=settings.AUTH_USER_MODEL,
                null=True,
                on_delete=models.SET_NULL,
            ),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name="postassertion",
            name="date_secondary_source",
            field=models.ForeignKey(
                related_name="postassertion_date_secondary_source",
                blank=True,
                to="promrep.SecondarySource",
                null=True,
                on_delete=models.SET_NULL,
            ),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name="postassertion",
            name="group",
            field=models.ForeignKey(
                blank=True, to="promrep.Group", null=True, on_delete=models.SET_NULL
            ),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name="postassertion",
            name="location",
            field=models.ForeignKey(
                blank=True, to="promrep.Location", null=True, on_delete=models.SET_NULL
            ),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name="postassertion",
            name="notes",
            field=models.ManyToManyField(
                to="promrep.PostAssertionNote",
                blank=True,
            ),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name="postassertion",
            name="office",
            field=models.ForeignKey(
                to="promrep.Office", null=True, on_delete=models.SET_NULL
            ),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name="postassertion",
            name="person",
            field=models.ForeignKey(
                to="promrep.Person", null=True, on_delete=models.SET_NULL
            ),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name="postassertion",
            name="role",
            field=models.ForeignKey(
                default=1, to="promrep.RoleType", null=True, on_delete=models.SET_NULL
            ),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name="postassertion",
            name="secondary_source",
            field=models.ForeignKey(
                to="promrep.SecondarySource", null=True, on_delete=models.SET_NULL
            ),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name="postassertion",
            name="updated_by",
            field=models.ForeignKey(
                related_name="postassertion_update",
                verbose_name="last updated by",
                blank=True,
                to=settings.AUTH_USER_MODEL,
                null=True,
                on_delete=models.SET_NULL,
            ),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name="person",
            name="date_secondary_source",
            field=models.ForeignKey(
                blank=True,
                to="promrep.SecondarySource",
                null=True,
                on_delete=models.SET_NULL,
            ),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name="person",
            name="gens",
            field=models.ForeignKey(
                blank=True, to="promrep.Gens", null=True, on_delete=models.SET_NULL
            ),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name="person",
            name="origin",
            field=models.ForeignKey(
                blank=True, to="promrep.Origin", null=True, on_delete=models.SET_NULL
            ),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name="person",
            name="praenomen",
            field=models.ForeignKey(
                blank=True, to="promrep.Praenomen", null=True, on_delete=models.SET_NULL
            ),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name="person",
            name="sex",
            field=models.ForeignKey(
                default=1,
                blank=True,
                to="promrep.Sex",
                null=True,
                on_delete=models.SET_NULL,
            ),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name="person",
            name="tribe",
            field=models.ForeignKey(
                blank=True, to="promrep.Tribe", null=True, on_delete=models.SET_NULL
            ),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name="person",
            name="updated_by",
            field=models.ForeignKey(
                related_name="person_update",
                verbose_name="last updated by",
                blank=True,
                to=settings.AUTH_USER_MODEL,
                null=True,
                on_delete=models.SET_NULL,
            ),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name="group",
            name="persons",
            field=models.ManyToManyField(
                to="promrep.Person", through="promrep.PostAssertion"
            ),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name="group",
            name="updated_by",
            field=models.ForeignKey(
                related_name="group_update",
                verbose_name="last updated by",
                blank=True,
                to=settings.AUTH_USER_MODEL,
                null=True,
                on_delete=models.SET_NULL,
            ),
            preserve_default=True,
        ),
    ]
