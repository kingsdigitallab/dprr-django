# -*- coding: utf-8 -*-
from django.db import models
from south.db import db

from south.v2 import SchemaMigration


class Migration(SchemaMigration):
    def forwards(self, orm):
        # Adding model 'HomePageAttachment'
        db.create_table(
            "wagtailbase_homepageattachment",
            (
                ("id", self.gf("django.db.models.fields.AutoField")(
                    primary_key=True)),
                (
                    "sort_order",
                    self.gf("django.db.models.fields.IntegerField")(
                        null=True, blank=True
                    ),
                ),
                (
                    "link_document",
                    self.gf("django.db.models.fields.related.ForeignKey")(
                        blank=True,
                        related_name="+",
                        null=True,
                        to=orm["wagtaildocs.Document"],
                    ),
                ),
                (
                    "link_external",
                    self.gf("django.db.models.fields.URLField")(
                        max_length=200, null=True, blank=True
                    ),
                ),
                (
                    "link_page",
                    self.gf("django.db.models.fields.related.ForeignKey")(
                        blank=True,
                        related_name="+",
                        null=True,
                        to=orm["wagtailcore.Page"],
                    ),
                ),
                (
                    "image",
                    self.gf("django.db.models.fields.related.ForeignKey")(
                        blank=True,
                        related_name="+",
                        null=True,
                        on_delete=models.SET_NULL,
                        to=orm["wagtailimages.Image"],
                    ),
                ),
                (
                    "embed_url",
                    self.gf("django.db.models.fields.URLField")(
                        max_length=200, blank=True
                    ),
                ),
                (
                    "caption",
                    self.gf("django.db.models.fields.CharField")(
                        max_length=255, blank=True
                    ),
                ),
                (
                    "page",
                    self.gf("modelcluster.fields.ParentalKey")(
                        related_name="attachments",
                        to=orm["wagtailbase.HomePage"]
                    ),
                ),
            ),
        )
        db.send_create_signal("wagtailbase", ["HomePageAttachment"])

        # Adding model 'BlogIndexPageAttachment'
        db.create_table(
            "wagtailbase_blogindexpageattachment",
            (
                ("id", self.gf("django.db.models.fields.AutoField")(
                    primary_key=True)),
                (
                    "sort_order",
                    self.gf("django.db.models.fields.IntegerField")(
                        null=True, blank=True
                    ),
                ),
                (
                    "link_document",
                    self.gf("django.db.models.fields.related.ForeignKey")(
                        blank=True,
                        related_name="+",
                        null=True,
                        to=orm["wagtaildocs.Document"],
                    ),
                ),
                (
                    "link_external",
                    self.gf("django.db.models.fields.URLField")(
                        max_length=200, null=True, blank=True
                    ),
                ),
                (
                    "link_page",
                    self.gf("django.db.models.fields.related.ForeignKey")(
                        blank=True,
                        related_name="+",
                        null=True,
                        to=orm["wagtailcore.Page"],
                    ),
                ),
                (
                    "image",
                    self.gf("django.db.models.fields.related.ForeignKey")(
                        blank=True,
                        related_name="+",
                        null=True,
                        on_delete=models.SET_NULL,
                        to=orm["wagtailimages.Image"],
                    ),
                ),
                (
                    "embed_url",
                    self.gf("django.db.models.fields.URLField")(
                        max_length=200, blank=True
                    ),
                ),
                (
                    "caption",
                    self.gf("django.db.models.fields.CharField")(
                        max_length=255, blank=True
                    ),
                ),
                (
                    "page",
                    self.gf("modelcluster.fields.ParentalKey")(
                        related_name="attachments",
                        to=orm["wagtailbase.BlogIndexPage"]
                    ),
                ),
            ),
        )
        db.send_create_signal("wagtailbase", ["BlogIndexPageAttachment"])

        # Adding model 'IndexPageAttachment'
        db.create_table(
            "wagtailbase_indexpageattachment",
            (
                ("id", self.gf("django.db.models.fields.AutoField")(
                    primary_key=True)),
                (
                    "sort_order",
                    self.gf("django.db.models.fields.IntegerField")(
                        null=True, blank=True
                    ),
                ),
                (
                    "link_document",
                    self.gf("django.db.models.fields.related.ForeignKey")(
                        blank=True,
                        related_name="+",
                        null=True,
                        to=orm["wagtaildocs.Document"],
                    ),
                ),
                (
                    "link_external",
                    self.gf("django.db.models.fields.URLField")(
                        max_length=200, null=True, blank=True
                    ),
                ),
                (
                    "link_page",
                    self.gf("django.db.models.fields.related.ForeignKey")(
                        blank=True,
                        related_name="+",
                        null=True,
                        to=orm["wagtailcore.Page"],
                    ),
                ),
                (
                    "image",
                    self.gf("django.db.models.fields.related.ForeignKey")(
                        blank=True,
                        related_name="+",
                        null=True,
                        on_delete=models.SET_NULL,
                        to=orm["wagtailimages.Image"],
                    ),
                ),
                (
                    "embed_url",
                    self.gf("django.db.models.fields.URLField")(
                        max_length=200, blank=True
                    ),
                ),
                (
                    "caption",
                    self.gf("django.db.models.fields.CharField")(
                        max_length=255, blank=True
                    ),
                ),
                (
                    "page",
                    self.gf("modelcluster.fields.ParentalKey")(
                        related_name="attachments",
                        to=orm["wagtailbase.IndexPage"]
                    ),
                ),
            ),
        )
        db.send_create_signal("wagtailbase", ["IndexPageAttachment"])

        # Adding model 'RichTextAttachment'
        db.create_table(
            "wagtailbase_richtextattachment",
            (
                ("id", self.gf("django.db.models.fields.AutoField")(
                    primary_key=True)),
                (
                    "sort_order",
                    self.gf("django.db.models.fields.IntegerField")(
                        null=True, blank=True
                    ),
                ),
                (
                    "link_document",
                    self.gf("django.db.models.fields.related.ForeignKey")(
                        blank=True,
                        related_name="+",
                        null=True,
                        to=orm["wagtaildocs.Document"],
                    ),
                ),
                (
                    "link_external",
                    self.gf("django.db.models.fields.URLField")(
                        max_length=200, null=True, blank=True
                    ),
                ),
                (
                    "link_page",
                    self.gf("django.db.models.fields.related.ForeignKey")(
                        blank=True,
                        related_name="+",
                        null=True,
                        to=orm["wagtailcore.Page"],
                    ),
                ),
                (
                    "image",
                    self.gf("django.db.models.fields.related.ForeignKey")(
                        blank=True,
                        related_name="+",
                        null=True,
                        on_delete=models.SET_NULL,
                        to=orm["wagtailimages.Image"],
                    ),
                ),
                (
                    "embed_url",
                    self.gf("django.db.models.fields.URLField")(
                        max_length=200, blank=True
                    ),
                ),
                (
                    "caption",
                    self.gf("django.db.models.fields.CharField")(
                        max_length=255, blank=True
                    ),
                ),
                (
                    "page",
                    self.gf("modelcluster.fields.ParentalKey")(
                        related_name="attachments",
                        to=orm["wagtailbase.RichTextPage"]
                    ),
                ),
            ),
        )
        db.send_create_signal("wagtailbase", ["RichTextAttachment"])

        # Adding model 'BlogPostAttachment'
        db.create_table(
            "wagtailbase_blogpostattachment",
            (
                ("id", self.gf("django.db.models.fields.AutoField")(
                    primary_key=True)),
                (
                    "sort_order",
                    self.gf("django.db.models.fields.IntegerField")(
                        null=True, blank=True
                    ),
                ),
                (
                    "link_document",
                    self.gf("django.db.models.fields.related.ForeignKey")(
                        blank=True,
                        related_name="+",
                        null=True,
                        to=orm["wagtaildocs.Document"],
                    ),
                ),
                (
                    "link_external",
                    self.gf("django.db.models.fields.URLField")(
                        max_length=200, null=True, blank=True
                    ),
                ),
                (
                    "link_page",
                    self.gf("django.db.models.fields.related.ForeignKey")(
                        blank=True,
                        related_name="+",
                        null=True,
                        to=orm["wagtailcore.Page"],
                    ),
                ),
                (
                    "image",
                    self.gf("django.db.models.fields.related.ForeignKey")(
                        blank=True,
                        related_name="+",
                        null=True,
                        on_delete=models.SET_NULL,
                        to=orm["wagtailimages.Image"],
                    ),
                ),
                (
                    "embed_url",
                    self.gf("django.db.models.fields.URLField")(
                        max_length=200, blank=True
                    ),
                ),
                (
                    "caption",
                    self.gf("django.db.models.fields.CharField")(
                        max_length=255, blank=True
                    ),
                ),
                (
                    "page",
                    self.gf("modelcluster.fields.ParentalKey")(
                        related_name="attachments",
                        to=orm["wagtailbase.BlogPost"]
                    ),
                ),
            ),
        )
        db.send_create_signal("wagtailbase", ["BlogPostAttachment"])

    def backwards(self, orm):
        # Deleting model 'HomePageAttachment'
        db.delete_table("wagtailbase_homepageattachment")

        # Deleting model 'BlogIndexPageAttachment'
        db.delete_table("wagtailbase_blogindexpageattachment")

        # Deleting model 'IndexPageAttachment'
        db.delete_table("wagtailbase_indexpageattachment")

        # Deleting model 'RichTextAttachment'
        db.delete_table("wagtailbase_richtextattachment")

        # Deleting model 'BlogPostAttachment'
        db.delete_table("wagtailbase_blogpostattachment")

    models = {
        "auth.group": {
            "Meta": {"object_name": "Group"},
            "id": (
                "django.db.models.fields.AutoField", [],
                {"primary_key": "True"}),
            "name": (
                "django.db.models.fields.CharField",
                [],
                {"unique": "True", "max_length": "80"},
            ),
            "permissions": (
                "django.db.models.fields.related.ManyToManyField",
                [],
                {
                    "to": "orm['auth.Permission']",
                    "symmetrical": "False",
                    "blank": "True",
                },
            ),
        },
        "auth.permission": {
            "Meta": {
                "ordering": "(u'content_type__app_label', "
                            "u'content_type__model', u'codename')",
                "unique_together": "((u'content_type', u'codename'),)",
                "object_name": "Permission",
            },
            "codename": (
                "django.db.models.fields.CharField",
                [],
                {"max_length": "100"},
            ),
            "content_type": (
                "django.db.models.fields.related.ForeignKey",
                [],
                {"to": "orm['contenttypes.ContentType']"},
            ),
            "id": (
                "django.db.models.fields.AutoField", [],
                {"primary_key": "True"}),
            "name": (
                "django.db.models.fields.CharField", [], {"max_length": "50"}),
        },
        "auth.user": {
            "Meta": {"object_name": "User"},
            "date_joined": (
                "django.db.models.fields.DateTimeField",
                [],
                {"default": "datetime.datetime.now"},
            ),
            "email": (
                "django.db.models.fields.EmailField",
                [],
                {"max_length": "75", "blank": "True"},
            ),
            "first_name": (
                "django.db.models.fields.CharField",
                [],
                {"max_length": "30", "blank": "True"},
            ),
            "groups": (
                "django.db.models.fields.related.ManyToManyField",
                [],
                {
                    "symmetrical": "False",
                    "related_name": "u'user_set'",
                    "blank": "True",
                    "to": "orm['auth.Group']",
                },
            ),
            "id": (
                "django.db.models.fields.AutoField", [],
                {"primary_key": "True"}),
            "is_active": (
                "django.db.models.fields.BooleanField",
                [],
                {"default": "True"},
            ),
            "is_staff": (
                "django.db.models.fields.BooleanField",
                [],
                {"default": "False"},
            ),
            "is_superuser": (
                "django.db.models.fields.BooleanField",
                [],
                {"default": "False"},
            ),
            "last_login": (
                "django.db.models.fields.DateTimeField",
                [],
                {"default": "datetime.datetime.now"},
            ),
            "last_name": (
                "django.db.models.fields.CharField",
                [],
                {"max_length": "30", "blank": "True"},
            ),
            "password": (
                "django.db.models.fields.CharField",
                [],
                {"max_length": "128"},
            ),
            "user_permissions": (
                "django.db.models.fields.related.ManyToManyField",
                [],
                {
                    "symmetrical": "False",
                    "related_name": "u'user_set'",
                    "blank": "True",
                    "to": "orm['auth.Permission']",
                },
            ),
            "username": (
                "django.db.models.fields.CharField",
                [],
                {"unique": "True", "max_length": "30"},
            ),
        },
        "contenttypes.contenttype": {
            "Meta": {
                "ordering": "('name',)",
                "unique_together": "(('app_label', 'model'),)",
                "object_name": "ContentType",
                "db_table": "'django_content_type'",
            },
            "app_label": (
                "django.db.models.fields.CharField",
                [],
                {"max_length": "100"},
            ),
            "id": (
                "django.db.models.fields.AutoField", [],
                {"primary_key": "True"}),
            "model": (
                "django.db.models.fields.CharField", [],
                {"max_length": "100"}),
            "name": (
                "django.db.models.fields.CharField", [],
                {"max_length": "100"}),
        },
        "taggit.tag": {
            "Meta": {"object_name": "Tag"},
            "id": (
                "django.db.models.fields.AutoField", [],
                {"primary_key": "True"}),
            "name": (
                "django.db.models.fields.CharField",
                [],
                {"unique": "True", "max_length": "100"},
            ),
            "slug": (
                "django.db.models.fields.SlugField",
                [],
                {"unique": "True", "max_length": "100"},
            ),
        },
        "wagtailbase.baseindexpage": {
            "Meta": {
                "object_name": "BaseIndexPage",
                "_ormbases": ["wagtailbase.BasePage"],
            },
            "basepage_ptr": (
                "django.db.models.fields.related.OneToOneField",
                [],
                {
                    "to": "orm['wagtailbase.BasePage']",
                    "unique": "True",
                    "primary_key": "True",
                },
            ),
            "introduction": (
                "wagtail.core.fields.RichTextField",
                [],
                {"blank": "True"},
            ),
        },
        "wagtailbase.basepage": {
            "Meta": {"object_name": "BasePage",
                     "_ormbases": ["wagtailcore.Page"]},
            "page_ptr": (
                "django.db.models.fields.related.OneToOneField",
                [],
                {
                    "to": "orm['wagtailcore.Page']",
                    "unique": "True",
                    "primary_key": "True",
                },
            ),
        },
        "wagtailbase.baserichtextpage": {
            "Meta": {
                "object_name": "BaseRichTextPage",
                "_ormbases": ["wagtailbase.BasePage"],
            },
            "basepage_ptr": (
                "django.db.models.fields.related.OneToOneField",
                [],
                {
                    "to": "orm['wagtailbase.BasePage']",
                    "unique": "True",
                    "primary_key": "True",
                },
            ),
            "content": ("wagtail.core.fields.RichTextField", [], {}),
        },
        "wagtailbase.blogindexpage": {
            "Meta": {
                "object_name": "BlogIndexPage",
                "_ormbases": ["wagtailbase.BaseIndexPage"],
            },
            "baseindexpage_ptr": (
                "django.db.models.fields.related.OneToOneField",
                [],
                {
                    "to": "orm['wagtailbase.BaseIndexPage']",
                    "unique": "True",
                    "primary_key": "True",
                },
            ),
        },
        "wagtailbase.blogindexpageattachment": {
            "Meta": {
                "ordering": "['sort_order']",
                "object_name": "BlogIndexPageAttachment",
            },
            "caption": (
                "django.db.models.fields.CharField",
                [],
                {"max_length": "255", "blank": "True"},
            ),
            "embed_url": (
                "django.db.models.fields.URLField",
                [],
                {"max_length": "200", "blank": "True"},
            ),
            "id": (
                "django.db.models.fields.AutoField", [],
                {"primary_key": "True"}),
            "image": (
                "django.db.models.fields.related.ForeignKey",
                [],
                {
                    "blank": "True",
                    "related_name": "'+'",
                    "null": "True",
                    "on_delete": "models.SET_NULL",
                    "to": "orm['wagtailimages.Image']",
                },
            ),
            "link_document": (
                "django.db.models.fields.related.ForeignKey",
                [],
                {
                    "blank": "True",
                    "related_name": "'+'",
                    "null": "True",
                    "to": "orm['wagtaildocs.Document']",
                },
            ),
            "link_external": (
                "django.db.models.fields.URLField",
                [],
                {"max_length": "200", "null": "True", "blank": "True"},
            ),
            "link_page": (
                "django.db.models.fields.related.ForeignKey",
                [],
                {
                    "blank": "True",
                    "related_name": "'+'",
                    "null": "True",
                    "to": "orm['wagtailcore.Page']",
                },
            ),
            "page": (
                "modelcluster.fields.ParentalKey",
                [],
                {
                    "related_name": "'attachments'",
                    "to": "orm['wagtailbase.BlogIndexPage']",
                },
            ),
            "sort_order": (
                "django.db.models.fields.IntegerField",
                [],
                {"null": "True", "blank": "True"},
            ),
        },
        "wagtailbase.blogindexpagerelatedlink": {
            "Meta": {
                "ordering": "['sort_order']",
                "object_name": "BlogIndexPageRelatedLink",
            },
            "id": (
                "django.db.models.fields.AutoField", [],
                {"primary_key": "True"}),
            "link_document": (
                "django.db.models.fields.related.ForeignKey",
                [],
                {
                    "blank": "True",
                    "related_name": "'+'",
                    "null": "True",
                    "to": "orm['wagtaildocs.Document']",
                },
            ),
            "link_external": (
                "django.db.models.fields.URLField",
                [],
                {"max_length": "200", "null": "True", "blank": "True"},
            ),
            "link_page": (
                "django.db.models.fields.related.ForeignKey",
                [],
                {
                    "blank": "True",
                    "related_name": "'+'",
                    "null": "True",
                    "to": "orm['wagtailcore.Page']",
                },
            ),
            "page": (
                "modelcluster.fields.ParentalKey",
                [],
                {
                    "related_name": "'related_links'",
                    "to": "orm['wagtailbase.BlogIndexPage']",
                },
            ),
            "sort_order": (
                "django.db.models.fields.IntegerField",
                [],
                {"null": "True", "blank": "True"},
            ),
            "title": (
                "django.db.models.fields.CharField", [],
                {"max_length": "256"}),
        },
        "wagtailbase.blogpost": {
            "Meta": {
                "object_name": "BlogPost",
                "_ormbases": ["wagtailbase.BaseRichTextPage"],
            },
            "baserichtextpage_ptr": (
                "django.db.models.fields.related.OneToOneField",
                [],
                {
                    "to": "orm['wagtailbase.BaseRichTextPage']",
                    "unique": "True",
                    "primary_key": "True",
                },
            ),
            "date": (
                "django.db.models.fields.DateField",
                [],
                {"default": "datetime.date.today"},
            ),
        },
        "wagtailbase.blogpostattachment": {
            "Meta": {"ordering": "['sort_order']",
                     "object_name": "BlogPostAttachment"},
            "caption": (
                "django.db.models.fields.CharField",
                [],
                {"max_length": "255", "blank": "True"},
            ),
            "embed_url": (
                "django.db.models.fields.URLField",
                [],
                {"max_length": "200", "blank": "True"},
            ),
            "id": (
                "django.db.models.fields.AutoField", [],
                {"primary_key": "True"}),
            "image": (
                "django.db.models.fields.related.ForeignKey",
                [],
                {
                    "blank": "True",
                    "related_name": "'+'",
                    "null": "True",
                    "on_delete": "models.SET_NULL",
                    "to": "orm['wagtailimages.Image']",
                },
            ),
            "link_document": (
                "django.db.models.fields.related.ForeignKey",
                [],
                {
                    "blank": "True",
                    "related_name": "'+'",
                    "null": "True",
                    "to": "orm['wagtaildocs.Document']",
                },
            ),
            "link_external": (
                "django.db.models.fields.URLField",
                [],
                {"max_length": "200", "null": "True", "blank": "True"},
            ),
            "link_page": (
                "django.db.models.fields.related.ForeignKey",
                [],
                {
                    "blank": "True",
                    "related_name": "'+'",
                    "null": "True",
                    "to": "orm['wagtailcore.Page']",
                },
            ),
            "page": (
                "modelcluster.fields.ParentalKey",
                [],
                {"related_name": "'attachments'",
                 "to": "orm['wagtailbase.BlogPost']"},
            ),
            "sort_order": (
                "django.db.models.fields.IntegerField",
                [],
                {"null": "True", "blank": "True"},
            ),
        },
        "wagtailbase.blogpostrelatedlink": {
            "Meta": {
                "ordering": "['sort_order']",
                "object_name": "BlogPostRelatedLink",
            },
            "id": (
                "django.db.models.fields.AutoField", [],
                {"primary_key": "True"}),
            "link_document": (
                "django.db.models.fields.related.ForeignKey",
                [],
                {
                    "blank": "True",
                    "related_name": "'+'",
                    "null": "True",
                    "to": "orm['wagtaildocs.Document']",
                },
            ),
            "link_external": (
                "django.db.models.fields.URLField",
                [],
                {"max_length": "200", "null": "True", "blank": "True"},
            ),
            "link_page": (
                "django.db.models.fields.related.ForeignKey",
                [],
                {
                    "blank": "True",
                    "related_name": "'+'",
                    "null": "True",
                    "to": "orm['wagtailcore.Page']",
                },
            ),
            "page": (
                "modelcluster.fields.ParentalKey",
                [],
                {
                    "related_name": "'related_links'",
                    "to": "orm['wagtailbase.BlogPost']",
                },
            ),
            "sort_order": (
                "django.db.models.fields.IntegerField",
                [],
                {"null": "True", "blank": "True"},
            ),
            "title": (
                "django.db.models.fields.CharField", [],
                {"max_length": "256"}),
        },
        "wagtailbase.blogposttag": {
            "Meta": {"object_name": "BlogPostTag"},
            "content_object": (
                "modelcluster.fields.ParentalKey",
                [],
                {"related_name": "'tagged_items'",
                 "to": "orm['wagtailbase.BlogPost']"},
            ),
            "id": (
                "django.db.models.fields.AutoField", [],
                {"primary_key": "True"}),
            "tag": (
                "django.db.models.fields.related.ForeignKey",
                [],
                {
                    "related_name": "u'wagtailbase_blogposttag_items'",
                    "to": "orm['taggit.Tag']",
                },
            ),
        },
        "wagtailbase.homepage": {
            "Meta": {
                "object_name": "HomePage",
                "_ormbases": ["wagtailbase.BaseRichTextPage"],
            },
            "baserichtextpage_ptr": (
                "django.db.models.fields.related.OneToOneField",
                [],
                {
                    "to": "orm['wagtailbase.BaseRichTextPage']",
                    "unique": "True",
                    "primary_key": "True",
                },
            ),
        },
        "wagtailbase.homepageattachment": {
            "Meta": {"ordering": "['sort_order']",
                     "object_name": "HomePageAttachment"},
            "caption": (
                "django.db.models.fields.CharField",
                [],
                {"max_length": "255", "blank": "True"},
            ),
            "embed_url": (
                "django.db.models.fields.URLField",
                [],
                {"max_length": "200", "blank": "True"},
            ),
            "id": (
                "django.db.models.fields.AutoField", [],
                {"primary_key": "True"}),
            "image": (
                "django.db.models.fields.related.ForeignKey",
                [],
                {
                    "blank": "True",
                    "related_name": "'+'",
                    "null": "True",
                    "on_delete": "models.SET_NULL",
                    "to": "orm['wagtailimages.Image']",
                },
            ),
            "link_document": (
                "django.db.models.fields.related.ForeignKey",
                [],
                {
                    "blank": "True",
                    "related_name": "'+'",
                    "null": "True",
                    "to": "orm['wagtaildocs.Document']",
                },
            ),
            "link_external": (
                "django.db.models.fields.URLField",
                [],
                {"max_length": "200", "null": "True", "blank": "True"},
            ),
            "link_page": (
                "django.db.models.fields.related.ForeignKey",
                [],
                {
                    "blank": "True",
                    "related_name": "'+'",
                    "null": "True",
                    "to": "orm['wagtailcore.Page']",
                },
            ),
            "page": (
                "modelcluster.fields.ParentalKey",
                [],
                {"related_name": "'attachments'",
                 "to": "orm['wagtailbase.HomePage']"},
            ),
            "sort_order": (
                "django.db.models.fields.IntegerField",
                [],
                {"null": "True", "blank": "True"},
            ),
        },
        "wagtailbase.indexpage": {
            "Meta": {
                "object_name": "IndexPage",
                "_ormbases": ["wagtailbase.BaseIndexPage"],
            },
            "baseindexpage_ptr": (
                "django.db.models.fields.related.OneToOneField",
                [],
                {
                    "to": "orm['wagtailbase.BaseIndexPage']",
                    "unique": "True",
                    "primary_key": "True",
                },
            ),
        },
        "wagtailbase.indexpageattachment": {
            "Meta": {
                "ordering": "['sort_order']",
                "object_name": "IndexPageAttachment",
            },
            "caption": (
                "django.db.models.fields.CharField",
                [],
                {"max_length": "255", "blank": "True"},
            ),
            "embed_url": (
                "django.db.models.fields.URLField",
                [],
                {"max_length": "200", "blank": "True"},
            ),
            "id": (
                "django.db.models.fields.AutoField", [],
                {"primary_key": "True"}),
            "image": (
                "django.db.models.fields.related.ForeignKey",
                [],
                {
                    "blank": "True",
                    "related_name": "'+'",
                    "null": "True",
                    "on_delete": "models.SET_NULL",
                    "to": "orm['wagtailimages.Image']",
                },
            ),
            "link_document": (
                "django.db.models.fields.related.ForeignKey",
                [],
                {
                    "blank": "True",
                    "related_name": "'+'",
                    "null": "True",
                    "to": "orm['wagtaildocs.Document']",
                },
            ),
            "link_external": (
                "django.db.models.fields.URLField",
                [],
                {"max_length": "200", "null": "True", "blank": "True"},
            ),
            "link_page": (
                "django.db.models.fields.related.ForeignKey",
                [],
                {
                    "blank": "True",
                    "related_name": "'+'",
                    "null": "True",
                    "to": "orm['wagtailcore.Page']",
                },
            ),
            "page": (
                "modelcluster.fields.ParentalKey",
                [],
                {"related_name": "'attachments'",
                 "to": "orm['wagtailbase.IndexPage']"},
            ),
            "sort_order": (
                "django.db.models.fields.IntegerField",
                [],
                {"null": "True", "blank": "True"},
            ),
        },
        "wagtailbase.indexpagerelatedlink": {
            "Meta": {
                "ordering": "['sort_order']",
                "object_name": "IndexPageRelatedLink",
            },
            "id": (
                "django.db.models.fields.AutoField", [],
                {"primary_key": "True"}),
            "link_document": (
                "django.db.models.fields.related.ForeignKey",
                [],
                {
                    "blank": "True",
                    "related_name": "'+'",
                    "null": "True",
                    "to": "orm['wagtaildocs.Document']",
                },
            ),
            "link_external": (
                "django.db.models.fields.URLField",
                [],
                {"max_length": "200", "null": "True", "blank": "True"},
            ),
            "link_page": (
                "django.db.models.fields.related.ForeignKey",
                [],
                {
                    "blank": "True",
                    "related_name": "'+'",
                    "null": "True",
                    "to": "orm['wagtailcore.Page']",
                },
            ),
            "page": (
                "modelcluster.fields.ParentalKey",
                [],
                {
                    "related_name": "'related_links'",
                    "to": "orm['wagtailbase.IndexPage']",
                },
            ),
            "sort_order": (
                "django.db.models.fields.IntegerField",
                [],
                {"null": "True", "blank": "True"},
            ),
            "title": (
                "django.db.models.fields.CharField", [],
                {"max_length": "256"}),
        },
        "wagtailbase.richtextattachment": {
            "Meta": {"ordering": "['sort_order']",
                     "object_name": "RichTextAttachment"},
            "caption": (
                "django.db.models.fields.CharField",
                [],
                {"max_length": "255", "blank": "True"},
            ),
            "embed_url": (
                "django.db.models.fields.URLField",
                [],
                {"max_length": "200", "blank": "True"},
            ),
            "id": (
                "django.db.models.fields.AutoField", [],
                {"primary_key": "True"}),
            "image": (
                "django.db.models.fields.related.ForeignKey",
                [],
                {
                    "blank": "True",
                    "related_name": "'+'",
                    "null": "True",
                    "on_delete": "models.SET_NULL",
                    "to": "orm['wagtailimages.Image']",
                },
            ),
            "link_document": (
                "django.db.models.fields.related.ForeignKey",
                [],
                {
                    "blank": "True",
                    "related_name": "'+'",
                    "null": "True",
                    "to": "orm['wagtaildocs.Document']",
                },
            ),
            "link_external": (
                "django.db.models.fields.URLField",
                [],
                {"max_length": "200", "null": "True", "blank": "True"},
            ),
            "link_page": (
                "django.db.models.fields.related.ForeignKey",
                [],
                {
                    "blank": "True",
                    "related_name": "'+'",
                    "null": "True",
                    "to": "orm['wagtailcore.Page']",
                },
            ),
            "page": (
                "modelcluster.fields.ParentalKey",
                [],
                {
                    "related_name": "'attachments'",
                    "to": "orm['wagtailbase.RichTextPage']",
                },
            ),
            "sort_order": (
                "django.db.models.fields.IntegerField",
                [],
                {"null": "True", "blank": "True"},
            ),
        },
        "wagtailbase.richtextpage": {
            "Meta": {
                "object_name": "RichTextPage",
                "_ormbases": ["wagtailbase.BaseRichTextPage"],
            },
            "baserichtextpage_ptr": (
                "django.db.models.fields.related.OneToOneField",
                [],
                {
                    "to": "orm['wagtailbase.BaseRichTextPage']",
                    "unique": "True",
                    "primary_key": "True",
                },
            ),
        },
        "wagtailbase.richtextpagerelatedlink": {
            "Meta": {
                "ordering": "['sort_order']",
                "object_name": "RichTextPageRelatedLink",
            },
            "id": (
                "django.db.models.fields.AutoField", [],
                {"primary_key": "True"}),
            "link_document": (
                "django.db.models.fields.related.ForeignKey",
                [],
                {
                    "blank": "True",
                    "related_name": "'+'",
                    "null": "True",
                    "to": "orm['wagtaildocs.Document']",
                },
            ),
            "link_external": (
                "django.db.models.fields.URLField",
                [],
                {"max_length": "200", "null": "True", "blank": "True"},
            ),
            "link_page": (
                "django.db.models.fields.related.ForeignKey",
                [],
                {
                    "blank": "True",
                    "related_name": "'+'",
                    "null": "True",
                    "to": "orm['wagtailcore.Page']",
                },
            ),
            "page": (
                "modelcluster.fields.ParentalKey",
                [],
                {
                    "related_name": "'related_links'",
                    "to": "orm['wagtailbase.RichTextPage']",
                },
            ),
            "sort_order": (
                "django.db.models.fields.IntegerField",
                [],
                {"null": "True", "blank": "True"},
            ),
            "title": (
                "django.db.models.fields.CharField", [],
                {"max_length": "256"}),
        },
        "wagtailcore.page": {
            "Meta": {"object_name": "Page"},
            "content_type": (
                "django.db.models.fields.related.ForeignKey",
                [],
                {"related_name": "'pages'",
                 "to": "orm['contenttypes.ContentType']"},
            ),
            "depth": ("django.db.models.fields.PositiveIntegerField", [], {}),
            "has_unpublished_changes": (
                "django.db.models.fields.BooleanField",
                [],
                {"default": "False"},
            ),
            "id": (
                "django.db.models.fields.AutoField", [],
                {"primary_key": "True"}),
            "live": (
                "django.db.models.fields.BooleanField", [],
                {"default": "True"}),
            "numchild": (
                "django.db.models.fields.PositiveIntegerField",
                [],
                {"default": "0"},
            ),
            "owner": (
                "django.db.models.fields.related.ForeignKey",
                [],
                {
                    "blank": "True",
                    "related_name": "'owned_pages'",
                    "null": "True",
                    "to": "orm['auth.User']",
                },
            ),
            "path": (
                "django.db.models.fields.CharField",
                [],
                {"unique": "True", "max_length": "255"},
            ),
            "search_description": (
                "django.db.models.fields.TextField",
                [],
                {"blank": "True"},
            ),
            "seo_title": (
                "django.db.models.fields.CharField",
                [],
                {"max_length": "255", "blank": "True"},
            ),
            "show_in_menus": (
                "django.db.models.fields.BooleanField",
                [],
                {"default": "False"},
            ),
            "slug": (
                "django.db.models.fields.SlugField", [], {"max_length": "50"}),
            "title": (
                "django.db.models.fields.CharField", [],
                {"max_length": "255"}),
            "url_path": (
                "django.db.models.fields.CharField",
                [],
                {"max_length": "255", "blank": "True"},
            ),
        },
        "wagtaildocs.document": {
            "Meta": {"object_name": "Document"},
            "created_at": (
                "django.db.models.fields.DateTimeField",
                [],
                {"auto_now_add": "True", "blank": "True"},
            ),
            "file": (
                "django.db.models.fields.files.FileField",
                [],
                {"max_length": "100"},
            ),
            "id": (
                "django.db.models.fields.AutoField", [],
                {"primary_key": "True"}),
            "title": (
                "django.db.models.fields.CharField", [],
                {"max_length": "255"}),
            "uploaded_by_user": (
                "django.db.models.fields.related.ForeignKey",
                [],
                {"to": "orm['auth.User']", "null": "True", "blank": "True"},
            ),
        },
        "wagtailimages.image": {
            "Meta": {"object_name": "Image"},
            "created_at": (
                "django.db.models.fields.DateTimeField",
                [],
                {"auto_now_add": "True", "blank": "True"},
            ),
            "file": (
                "django.db.models.fields.files.ImageField",
                [],
                {"max_length": "100"},
            ),
            "height": ("django.db.models.fields.IntegerField", [], {}),
            "id": (
                "django.db.models.fields.AutoField", [],
                {"primary_key": "True"}),
            "title": (
                "django.db.models.fields.CharField", [],
                {"max_length": "255"}),
            "uploaded_by_user": (
                "django.db.models.fields.related.ForeignKey",
                [],
                {"to": "orm['auth.User']", "null": "True", "blank": "True"},
            ),
            "width": ("django.db.models.fields.IntegerField", [], {}),
        },
    }

    complete_apps = ["wagtailbase"]
