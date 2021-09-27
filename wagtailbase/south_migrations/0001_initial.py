# -*- coding: utf-8 -*-

from south.db import db
from south.utils import datetime_utils as datetime
from south.v2 import SchemaMigration


class Migration(SchemaMigration):
    def forwards(self, orm):
        # Adding model 'BasePage'
        db.create_table(
            "wagtailbase_basepage",
            (
                (
                    "page_ptr",
                    self.gf("django.db.models.fields.related.OneToOneField")(
                        to=orm["wagtailcore.Page"], unique=True,
                        primary_key=True
                    ),
                ),
            ),
        )
        db.send_create_signal("wagtailbase", ["BasePage"])

        # Adding model 'BaseIndexPage'
        db.create_table(
            "wagtailbase_baseindexpage",
            (
                (
                    "basepage_ptr",
                    self.gf("django.db.models.fields.related.OneToOneField")(
                        to=orm["wagtailbase.BasePage"], unique=True,
                        primary_key=True
                    ),
                ),
                (
                    "introduction",
                    self.gf("wagtail.core.fields.RichTextField")(blank=True),
                ),
            ),
        )
        db.send_create_signal("wagtailbase", ["BaseIndexPage"])

        # Adding model 'BaseRichTextPage'
        db.create_table(
            "wagtailbase_baserichtextpage",
            (
                (
                    "basepage_ptr",
                    self.gf("django.db.models.fields.related.OneToOneField")(
                        to=orm["wagtailbase.BasePage"], unique=True,
                        primary_key=True
                    ),
                ),
                ("content", self.gf("wagtail.core.fields.RichTextField")()),
            ),
        )
        db.send_create_signal("wagtailbase", ["BaseRichTextPage"])

        # Adding model 'IndexPage'
        db.create_table(
            "wagtailbase_indexpage",
            (
                (
                    "baseindexpage_ptr",
                    self.gf("django.db.models.fields.related.OneToOneField")(
                        to=orm["wagtailbase.BaseIndexPage"],
                        unique=True,
                        primary_key=True,
                    ),
                ),
            ),
        )
        db.send_create_signal("wagtailbase", ["IndexPage"])

        # Adding model 'IndexPageRelatedLink'
        db.create_table(
            "wagtailbase_indexpagerelatedlink",
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
                ("title",
                 self.gf("django.db.models.fields.CharField")(max_length=256)),
                (
                    "page",
                    self.gf("modelcluster.fields.ParentalKey")(
                        related_name="related_links",
                        to=orm["wagtailbase.IndexPage"]
                    ),
                ),
            ),
        )
        db.send_create_signal("wagtailbase", ["IndexPageRelatedLink"])

        # Adding model 'RichTextPage'
        db.create_table(
            "wagtailbase_richtextpage",
            (
                (
                    "baserichtextpage_ptr",
                    self.gf("django.db.models.fields.related.OneToOneField")(
                        to=orm["wagtailbase.BaseRichTextPage"],
                        unique=True,
                        primary_key=True,
                    ),
                ),
            ),
        )
        db.send_create_signal("wagtailbase", ["RichTextPage"])

        # Adding model 'RichTextPageRelatedLink'
        db.create_table(
            "wagtailbase_richtextpagerelatedlink",
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
                ("title",
                 self.gf("django.db.models.fields.CharField")(max_length=256)),
                (
                    "page",
                    self.gf("modelcluster.fields.ParentalKey")(
                        related_name="related_links",
                        to=orm["wagtailbase.RichTextPage"]
                    ),
                ),
            ),
        )
        db.send_create_signal("wagtailbase", ["RichTextPageRelatedLink"])

        # Adding model 'HomePage'
        db.create_table(
            "wagtailbase_homepage",
            (
                (
                    "baserichtextpage_ptr",
                    self.gf("django.db.models.fields.related.OneToOneField")(
                        to=orm["wagtailbase.BaseRichTextPage"],
                        unique=True,
                        primary_key=True,
                    ),
                ),
            ),
        )
        db.send_create_signal("wagtailbase", ["HomePage"])

        # Adding model 'BlogIndexPage'
        db.create_table(
            "wagtailbase_blogindexpage",
            (
                (
                    "baseindexpage_ptr",
                    self.gf("django.db.models.fields.related.OneToOneField")(
                        to=orm["wagtailbase.BaseIndexPage"],
                        unique=True,
                        primary_key=True,
                    ),
                ),
            ),
        )
        db.send_create_signal("wagtailbase", ["BlogIndexPage"])

        # Adding model 'BlogIndexPageRelatedLink'
        db.create_table(
            "wagtailbase_blogindexpagerelatedlink",
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
                ("title",
                 self.gf("django.db.models.fields.CharField")(max_length=256)),
                (
                    "page",
                    self.gf("modelcluster.fields.ParentalKey")(
                        related_name="related_links",
                        to=orm["wagtailbase.BlogIndexPage"],
                    ),
                ),
            ),
        )
        db.send_create_signal("wagtailbase", ["BlogIndexPageRelatedLink"])

        # Adding model 'BlogPostTag'
        db.create_table(
            "wagtailbase_blogposttag",
            (
                ("id", self.gf("django.db.models.fields.AutoField")(
                    primary_key=True)),
                (
                    "tag",
                    self.gf("django.db.models.fields.related.ForeignKey")(
                        related_name="wagtailbase_blogposttag_items",
                        to=orm["taggit.Tag"],
                    ),
                ),
                (
                    "content_object",
                    self.gf("modelcluster.fields.ParentalKey")(
                        related_name="tagged_items",
                        to=orm["wagtailbase.BlogPost"]
                    ),
                ),
            ),
        )
        db.send_create_signal("wagtailbase", ["BlogPostTag"])

        # Adding model 'BlogPost'
        db.create_table(
            "wagtailbase_blogpost",
            (
                (
                    "baserichtextpage_ptr",
                    self.gf("django.db.models.fields.related.OneToOneField")(
                        to=orm["wagtailbase.BaseRichTextPage"],
                        unique=True,
                        primary_key=True,
                    ),
                ),
                (
                    "date",
                    self.gf("django.db.models.fields.DateField")(
                        default=datetime.date.today
                    ),
                ),
            ),
        )
        db.send_create_signal("wagtailbase", ["BlogPost"])

        # Adding model 'BlogPostRelatedLink'
        db.create_table(
            "wagtailbase_blogpostrelatedlink",
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
                ("title",
                 self.gf("django.db.models.fields.CharField")(max_length=256)),
                (
                    "page",
                    self.gf("modelcluster.fields.ParentalKey")(
                        related_name="related_links",
                        to=orm["wagtailbase.BlogPost"]
                    ),
                ),
            ),
        )
        db.send_create_signal("wagtailbase", ["BlogPostRelatedLink"])

    def backwards(self, orm):
        # Deleting model 'BasePage'
        db.delete_table("wagtailbase_basepage")

        # Deleting model 'BaseIndexPage'
        db.delete_table("wagtailbase_baseindexpage")

        # Deleting model 'BaseRichTextPage'
        db.delete_table("wagtailbase_baserichtextpage")

        # Deleting model 'IndexPage'
        db.delete_table("wagtailbase_indexpage")

        # Deleting model 'IndexPageRelatedLink'
        db.delete_table("wagtailbase_indexpagerelatedlink")

        # Deleting model 'RichTextPage'
        db.delete_table("wagtailbase_richtextpage")

        # Deleting model 'RichTextPageRelatedLink'
        db.delete_table("wagtailbase_richtextpagerelatedlink")

        # Deleting model 'HomePage'
        db.delete_table("wagtailbase_homepage")

        # Deleting model 'BlogIndexPage'
        db.delete_table("wagtailbase_blogindexpage")

        # Deleting model 'BlogIndexPageRelatedLink'
        db.delete_table("wagtailbase_blogindexpagerelatedlink")

        # Deleting model 'BlogPostTag'
        db.delete_table("wagtailbase_blogposttag")

        # Deleting model 'BlogPost'
        db.delete_table("wagtailbase_blogpost")

        # Deleting model 'BlogPostRelatedLink'
        db.delete_table("wagtailbase_blogpostrelatedlink")

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
    }

    complete_apps = ["wagtailbase"]
