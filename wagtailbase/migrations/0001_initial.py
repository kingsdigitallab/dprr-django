# -*- coding: utf-8 -*-


import datetime

import django.db.models.deletion
import modelcluster.fields
import modelcluster.tags
import wagtail.core.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("wagtailimages", "0002_initial_data"),
        ("wagtaildocs", "0002_initial_data"),
        ("wagtailcore", "0002_initial_data"),
        ("taggit", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="BasePage",
            fields=[
                (
                    "page_ptr",
                    models.OneToOneField(
                        parent_link=True,
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        to="wagtailcore.Page",
                        on_delete=models.CASCADE
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=("wagtailcore.page",),
        ),
        migrations.CreateModel(
            name="BaseIndexPage",
            fields=[
                (
                    "basepage_ptr",
                    models.OneToOneField(
                        parent_link=True,
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        to="wagtailbase.BasePage",
                        on_delete=models.CASCADE
                    ),
                ),
                ("introduction", wagtail.core.fields.RichTextField(blank=True)),
            ],
            options={
                "abstract": False,
            },
            bases=("wagtailbase.basepage",),
        ),
        migrations.CreateModel(
            name="BaseRichTextPage",
            fields=[
                (
                    "basepage_ptr",
                    models.OneToOneField(
                        parent_link=True,
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        to="wagtailbase.BasePage",
                        on_delete=models.CASCADE
                    ),
                ),
                ("content", wagtail.core.fields.RichTextField()),
            ],
            options={
                "abstract": False,
            },
            bases=("wagtailbase.basepage",),
        ),
        migrations.CreateModel(
            name="BlogIndexPage",
            fields=[
                (
                    "baseindexpage_ptr",
                    models.OneToOneField(
                        parent_link=True,
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        to="wagtailbase.BaseIndexPage",
                        on_delete=models.CASCADE
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=("wagtailbase.baseindexpage",),
        ),
        migrations.CreateModel(
            name="BlogIndexPageAttachment",
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
                    "sort_order",
                    models.IntegerField(null=True, editable=False, blank=True),
                ),
                (
                    "link_external",
                    models.URLField(
                        null=True, verbose_name="External link", blank=True
                    ),
                ),
                ("embed_url", models.URLField(verbose_name="Embed URL", blank=True)),
                ("caption", models.CharField(max_length=255, blank=True)),
                (
                    "image",
                    models.ForeignKey(
                        related_name="+",
                        on_delete=django.db.models.deletion.SET_NULL,
                        blank=True,
                        to="wagtailimages.Image",
                        null=True,
                    ),
                ),
                (
                    "link_document",
                    models.ForeignKey(
                        related_name="+",
                        blank=True,
                        to="wagtaildocs.Document",
                        null=True, on_delete=models.SET_NULL,
                    ),
                ),
                (
                    "link_page",
                    models.ForeignKey(
                        related_name="+", blank=True, to="wagtailcore.Page",
                        null=True, on_delete=models.SET_NULL
                    ),
                ),
                (
                    "page",
                    modelcluster.fields.ParentalKey(
                        related_name="attachments", to="wagtailbase.BlogIndexPage"
                    ),
                ),
            ],
            options={
                "ordering": ["sort_order"],
                "abstract": False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name="BlogIndexPageRelatedLink",
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
                    "sort_order",
                    models.IntegerField(null=True, editable=False, blank=True),
                ),
                (
                    "link_external",
                    models.URLField(
                        null=True, verbose_name="External link", blank=True
                    ),
                ),
                ("title", models.CharField(help_text="Link title", max_length=256)),
                (
                    "link_document",
                    models.ForeignKey(
                        related_name="+",
                        blank=True,
                        to="wagtaildocs.Document",
                        null=True,
                        on_delete=models.SET_NULL
                    ),
                ),
                (
                    "link_page",
                    models.ForeignKey(
                        related_name="+", blank=True,
                        to="wagtailcore.Page", null=True,
                        on_delete=models.SET_NULL
                    ),
                ),
                (
                    "page",
                    modelcluster.fields.ParentalKey(
                        related_name="related_links", to="wagtailbase.BlogIndexPage"
                    ),
                ),
            ],
            options={
                "ordering": ["sort_order"],
                "abstract": False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name="BlogPost",
            fields=[
                (
                    "baserichtextpage_ptr",
                    models.OneToOneField(
                        parent_link=True,
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        to="wagtailbase.BaseRichTextPage",
                        on_delete=models.CASCADE
                    ),
                ),
                (
                    "date",
                    models.DateField(
                        default=datetime.date.today, verbose_name="Post Date"
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=("wagtailbase.baserichtextpage",),
        ),
        migrations.CreateModel(
            name="BlogPostAttachment",
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
                    "sort_order",
                    models.IntegerField(null=True, editable=False, blank=True),
                ),
                (
                    "link_external",
                    models.URLField(
                        null=True, verbose_name="External link", blank=True
                    ),
                ),
                ("embed_url", models.URLField(verbose_name="Embed URL", blank=True)),
                ("caption", models.CharField(max_length=255, blank=True)),
                (
                    "image",
                    models.ForeignKey(
                        related_name="+",
                        on_delete=django.db.models.deletion.SET_NULL,
                        blank=True,
                        to="wagtailimages.Image",
                        null=True,
                    ),
                ),
                (
                    "link_document",
                    models.ForeignKey(
                        related_name="+",
                        blank=True,
                        to="wagtaildocs.Document",
                        null=True, on_delete=models.SET_NULL
                    ),
                ),
                (
                    "link_page",
                    models.ForeignKey(
                        related_name="+", blank=True,
                        to="wagtailcore.Page", null=True,
                        on_delete=models.SET_NULL
                    ),
                ),
                (
                    "page",
                    modelcluster.fields.ParentalKey(
                        related_name="attachments", to="wagtailbase.BlogPost"
                    ),
                ),
            ],
            options={
                "ordering": ["sort_order"],
                "abstract": False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name="BlogPostRelatedLink",
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
                    "sort_order",
                    models.IntegerField(null=True, editable=False, blank=True),
                ),
                (
                    "link_external",
                    models.URLField(
                        null=True, verbose_name="External link", blank=True
                    ),
                ),
                ("title", models.CharField(help_text="Link title", max_length=256)),
                (
                    "link_document",
                    models.ForeignKey(
                        related_name="+",
                        blank=True,
                        to="wagtaildocs.Document",
                        null=True, on_delete=models.SET_NULL
                    ),
                ),
                (
                    "link_page",
                    models.ForeignKey(
                        related_name="+", blank=True, to="wagtailcore.Page",
                        null=True, on_delete=models.SET_NULL
                    ),
                ),
                (
                    "page",
                    modelcluster.fields.ParentalKey(
                        related_name="related_links", to="wagtailbase.BlogPost"
                    ),
                ),
            ],
            options={
                "ordering": ["sort_order"],
                "abstract": False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name="BlogPostTag",
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
                    "content_object",
                    modelcluster.fields.ParentalKey(
                        related_name="tagged_items", to="wagtailbase.BlogPost"
                    ),
                ),
                (
                    "tag",
                    models.ForeignKey(
                        related_name="wagtailbase_blogposttag_items",
                        to="taggit.Tag", on_delete=models.CASCADE
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name="HomePage",
            fields=[
                (
                    "baserichtextpage_ptr",
                    models.OneToOneField(
                        parent_link=True,
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        to="wagtailbase.BaseRichTextPage",
                        on_delete=models.CASCADE
                    ),
                ),
            ],
            options={
                "verbose_name": "Homepage",
            },
            bases=("wagtailbase.baserichtextpage",),
        ),
        migrations.CreateModel(
            name="HomePageAttachment",
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
                    "sort_order",
                    models.IntegerField(null=True, editable=False, blank=True),
                ),
                (
                    "link_external",
                    models.URLField(
                        null=True, verbose_name="External link", blank=True
                    ),
                ),
                ("embed_url", models.URLField(verbose_name="Embed URL", blank=True)),
                ("caption", models.CharField(max_length=255, blank=True)),
                (
                    "image",
                    models.ForeignKey(
                        related_name="+",
                        on_delete=django.db.models.deletion.SET_NULL,
                        blank=True,
                        to="wagtailimages.Image",
                        null=True,
                    ),
                ),
                (
                    "link_document",
                    models.ForeignKey(
                        related_name="+",
                        blank=True,
                        to="wagtaildocs.Document",
                        null=True, on_delete=models.SET_NULL
                    ),
                ),
                (
                    "link_page",
                    models.ForeignKey(
                        related_name="+", blank=True, to="wagtailcore.Page",
                        null=True, on_delete=models.SET_NULL
                    ),
                ),
                (
                    "page",
                    modelcluster.fields.ParentalKey(
                        related_name="attachments", to="wagtailbase.HomePage"
                    ),
                ),
            ],
            options={
                "ordering": ["sort_order"],
                "abstract": False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name="IndexPage",
            fields=[
                (
                    "baseindexpage_ptr",
                    models.OneToOneField(
                        parent_link=True,
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        to="wagtailbase.BaseIndexPage",
                        on_delete=models.CASCADE
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=("wagtailbase.baseindexpage",),
        ),
        migrations.CreateModel(
            name="IndexPageAttachment",
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
                    "sort_order",
                    models.IntegerField(null=True, editable=False, blank=True),
                ),
                (
                    "link_external",
                    models.URLField(
                        null=True, verbose_name="External link", blank=True
                    ),
                ),
                ("embed_url", models.URLField(verbose_name="Embed URL", blank=True)),
                ("caption", models.CharField(max_length=255, blank=True)),
                (
                    "image",
                    models.ForeignKey(
                        related_name="+",
                        on_delete=django.db.models.deletion.SET_NULL,
                        blank=True,
                        to="wagtailimages.Image",
                        null=True,
                    ),
                ),
                (
                    "link_document",
                    models.ForeignKey(
                        related_name="+",
                        blank=True,
                        to="wagtaildocs.Document",
                        null=True, on_delete=models.SET_NULL
                    ),
                ),
                (
                    "link_page",
                    models.ForeignKey(
                        related_name="+", blank=True, to="wagtailcore.Page",
                        null=True, on_delete=models.SET_NULL
                    ),
                ),
                (
                    "page",
                    modelcluster.fields.ParentalKey(
                        related_name="attachments", to="wagtailbase.IndexPage"
                    ),
                ),
            ],
            options={
                "ordering": ["sort_order"],
                "abstract": False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name="IndexPageRelatedLink",
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
                    "sort_order",
                    models.IntegerField(null=True, editable=False, blank=True),
                ),
                (
                    "link_external",
                    models.URLField(
                        null=True, verbose_name="External link", blank=True
                    ),
                ),
                ("title", models.CharField(help_text="Link title", max_length=256)),
                (
                    "link_document",
                    models.ForeignKey(
                        related_name="+",
                        blank=True,
                        to="wagtaildocs.Document",
                        null=True, on_delete=models.SET_NULL
                    ),
                ),
                (
                    "link_page",
                    models.ForeignKey(
                        related_name="+", blank=True, to="wagtailcore.Page",
                        null=True, on_delete=models.SET_NULL
                    ),
                ),
                (
                    "page",
                    modelcluster.fields.ParentalKey(
                        related_name="related_links", to="wagtailbase.IndexPage"
                    ),
                ),
            ],
            options={
                "ordering": ["sort_order"],
                "abstract": False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name="RichTextAttachment",
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
                    "sort_order",
                    models.IntegerField(null=True, editable=False, blank=True),
                ),
                (
                    "link_external",
                    models.URLField(
                        null=True, verbose_name="External link", blank=True
                    ),
                ),
                ("embed_url", models.URLField(verbose_name="Embed URL", blank=True)),
                ("caption", models.CharField(max_length=255, blank=True)),
                (
                    "image",
                    models.ForeignKey(
                        related_name="+",
                        on_delete=django.db.models.deletion.SET_NULL,
                        blank=True,
                        to="wagtailimages.Image",
                        null=True,
                    ),
                ),
                (
                    "link_document",
                    models.ForeignKey(
                        related_name="+",
                        blank=True,
                        to="wagtaildocs.Document",
                        null=True, on_delete=models.SET_NULL
                    ),
                ),
                (
                    "link_page",
                    models.ForeignKey(
                        related_name="+", blank=True, to="wagtailcore.Page",
                        null=True, on_delete=models.SET_NULL
                    ),
                ),
            ],
            options={
                "ordering": ["sort_order"],
                "abstract": False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name="RichTextPage",
            fields=[
                (
                    "baserichtextpage_ptr",
                    models.OneToOneField(
                        parent_link=True,
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        to="wagtailbase.BaseRichTextPage",
                        on_delete=models.CASCADE
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=("wagtailbase.baserichtextpage",),
        ),
        migrations.CreateModel(
            name="RichTextPageRelatedLink",
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
                    "sort_order",
                    models.IntegerField(null=True, editable=False, blank=True),
                ),
                (
                    "link_external",
                    models.URLField(
                        null=True, verbose_name="External link", blank=True
                    ),
                ),
                ("title", models.CharField(help_text="Link title", max_length=256)),
                (
                    "link_document",
                    models.ForeignKey(
                        related_name="+",
                        blank=True,
                        to="wagtaildocs.Document",
                        null=True, on_delete=models.SET_NULL
                    ),
                ),
                (
                    "link_page",
                    models.ForeignKey(
                        related_name="+", blank=True, to="wagtailcore.Page",
                        null=True, on_delete=models.SET_NULL
                    ),
                ),
                (
                    "page",
                    modelcluster.fields.ParentalKey(
                        related_name="related_links", to="wagtailbase.RichTextPage"
                    ),
                ),
            ],
            options={
                "ordering": ["sort_order"],
                "abstract": False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name="richtextattachment",
            name="page",
            field=modelcluster.fields.ParentalKey(
                related_name="attachments", to="wagtailbase.RichTextPage"
            ),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name="blogpost",
            name="tags",
            field=modelcluster.tags.ClusterTaggableManager(
                to="taggit.Tag",
                through="wagtailbase.BlogPostTag",
                blank=True,
                help_text="A comma-separated list of tags.",
                verbose_name="Tags",
            ),
            preserve_default=True,
        ),
    ]
