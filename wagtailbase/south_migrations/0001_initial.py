# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'BasePage'
        db.create_table(u'wagtailbase_basepage', (
            (u'page_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['wagtailcore.Page'], unique=True, primary_key=True)),
        ))
        db.send_create_signal(u'wagtailbase', ['BasePage'])

        # Adding model 'BaseIndexPage'
        db.create_table(u'wagtailbase_baseindexpage', (
            (u'basepage_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['wagtailbase.BasePage'], unique=True, primary_key=True)),
            ('introduction', self.gf('wagtail.wagtailcore.fields.RichTextField')(blank=True)),
        ))
        db.send_create_signal(u'wagtailbase', ['BaseIndexPage'])

        # Adding model 'BaseRichTextPage'
        db.create_table(u'wagtailbase_baserichtextpage', (
            (u'basepage_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['wagtailbase.BasePage'], unique=True, primary_key=True)),
            ('content', self.gf('wagtail.wagtailcore.fields.RichTextField')()),
        ))
        db.send_create_signal(u'wagtailbase', ['BaseRichTextPage'])

        # Adding model 'IndexPage'
        db.create_table(u'wagtailbase_indexpage', (
            (u'baseindexpage_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['wagtailbase.BaseIndexPage'], unique=True, primary_key=True)),
        ))
        db.send_create_signal(u'wagtailbase', ['IndexPage'])

        # Adding model 'IndexPageRelatedLink'
        db.create_table(u'wagtailbase_indexpagerelatedlink', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sort_order', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('link_document', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='+', null=True, to=orm['wagtaildocs.Document'])),
            ('link_external', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('link_page', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='+', null=True, to=orm['wagtailcore.Page'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('page', self.gf('modelcluster.fields.ParentalKey')(related_name='related_links', to=orm['wagtailbase.IndexPage'])),
        ))
        db.send_create_signal(u'wagtailbase', ['IndexPageRelatedLink'])

        # Adding model 'RichTextPage'
        db.create_table(u'wagtailbase_richtextpage', (
            (u'baserichtextpage_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['wagtailbase.BaseRichTextPage'], unique=True, primary_key=True)),
        ))
        db.send_create_signal(u'wagtailbase', ['RichTextPage'])

        # Adding model 'RichTextPageRelatedLink'
        db.create_table(u'wagtailbase_richtextpagerelatedlink', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sort_order', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('link_document', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='+', null=True, to=orm['wagtaildocs.Document'])),
            ('link_external', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('link_page', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='+', null=True, to=orm['wagtailcore.Page'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('page', self.gf('modelcluster.fields.ParentalKey')(related_name='related_links', to=orm['wagtailbase.RichTextPage'])),
        ))
        db.send_create_signal(u'wagtailbase', ['RichTextPageRelatedLink'])

        # Adding model 'HomePage'
        db.create_table(u'wagtailbase_homepage', (
            (u'baserichtextpage_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['wagtailbase.BaseRichTextPage'], unique=True, primary_key=True)),
        ))
        db.send_create_signal(u'wagtailbase', ['HomePage'])

        # Adding model 'BlogIndexPage'
        db.create_table(u'wagtailbase_blogindexpage', (
            (u'baseindexpage_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['wagtailbase.BaseIndexPage'], unique=True, primary_key=True)),
        ))
        db.send_create_signal(u'wagtailbase', ['BlogIndexPage'])

        # Adding model 'BlogIndexPageRelatedLink'
        db.create_table(u'wagtailbase_blogindexpagerelatedlink', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sort_order', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('link_document', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='+', null=True, to=orm['wagtaildocs.Document'])),
            ('link_external', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('link_page', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='+', null=True, to=orm['wagtailcore.Page'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('page', self.gf('modelcluster.fields.ParentalKey')(related_name='related_links', to=orm['wagtailbase.BlogIndexPage'])),
        ))
        db.send_create_signal(u'wagtailbase', ['BlogIndexPageRelatedLink'])

        # Adding model 'BlogPostTag'
        db.create_table(u'wagtailbase_blogposttag', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tag', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'wagtailbase_blogposttag_items', to=orm['taggit.Tag'])),
            ('content_object', self.gf('modelcluster.fields.ParentalKey')(related_name='tagged_items', to=orm['wagtailbase.BlogPost'])),
        ))
        db.send_create_signal(u'wagtailbase', ['BlogPostTag'])

        # Adding model 'BlogPost'
        db.create_table(u'wagtailbase_blogpost', (
            (u'baserichtextpage_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['wagtailbase.BaseRichTextPage'], unique=True, primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateField')(default=datetime.date.today)),
        ))
        db.send_create_signal(u'wagtailbase', ['BlogPost'])

        # Adding model 'BlogPostRelatedLink'
        db.create_table(u'wagtailbase_blogpostrelatedlink', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sort_order', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('link_document', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='+', null=True, to=orm['wagtaildocs.Document'])),
            ('link_external', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('link_page', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='+', null=True, to=orm['wagtailcore.Page'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('page', self.gf('modelcluster.fields.ParentalKey')(related_name='related_links', to=orm['wagtailbase.BlogPost'])),
        ))
        db.send_create_signal(u'wagtailbase', ['BlogPostRelatedLink'])


    def backwards(self, orm):
        # Deleting model 'BasePage'
        db.delete_table(u'wagtailbase_basepage')

        # Deleting model 'BaseIndexPage'
        db.delete_table(u'wagtailbase_baseindexpage')

        # Deleting model 'BaseRichTextPage'
        db.delete_table(u'wagtailbase_baserichtextpage')

        # Deleting model 'IndexPage'
        db.delete_table(u'wagtailbase_indexpage')

        # Deleting model 'IndexPageRelatedLink'
        db.delete_table(u'wagtailbase_indexpagerelatedlink')

        # Deleting model 'RichTextPage'
        db.delete_table(u'wagtailbase_richtextpage')

        # Deleting model 'RichTextPageRelatedLink'
        db.delete_table(u'wagtailbase_richtextpagerelatedlink')

        # Deleting model 'HomePage'
        db.delete_table(u'wagtailbase_homepage')

        # Deleting model 'BlogIndexPage'
        db.delete_table(u'wagtailbase_blogindexpage')

        # Deleting model 'BlogIndexPageRelatedLink'
        db.delete_table(u'wagtailbase_blogindexpagerelatedlink')

        # Deleting model 'BlogPostTag'
        db.delete_table(u'wagtailbase_blogposttag')

        # Deleting model 'BlogPost'
        db.delete_table(u'wagtailbase_blogpost')

        # Deleting model 'BlogPostRelatedLink'
        db.delete_table(u'wagtailbase_blogpostrelatedlink')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'taggit.tag': {
            'Meta': {'object_name': 'Tag'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100'})
        },
        u'wagtailbase.baseindexpage': {
            'Meta': {'object_name': 'BaseIndexPage', '_ormbases': [u'wagtailbase.BasePage']},
            u'basepage_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['wagtailbase.BasePage']", 'unique': 'True', 'primary_key': 'True'}),
            'introduction': ('wagtail.wagtailcore.fields.RichTextField', [], {'blank': 'True'})
        },
        u'wagtailbase.basepage': {
            'Meta': {'object_name': 'BasePage', '_ormbases': [u'wagtailcore.Page']},
            u'page_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['wagtailcore.Page']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'wagtailbase.baserichtextpage': {
            'Meta': {'object_name': 'BaseRichTextPage', '_ormbases': [u'wagtailbase.BasePage']},
            u'basepage_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['wagtailbase.BasePage']", 'unique': 'True', 'primary_key': 'True'}),
            'content': ('wagtail.wagtailcore.fields.RichTextField', [], {})
        },
        u'wagtailbase.blogindexpage': {
            'Meta': {'object_name': 'BlogIndexPage', '_ormbases': [u'wagtailbase.BaseIndexPage']},
            u'baseindexpage_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['wagtailbase.BaseIndexPage']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'wagtailbase.blogindexpagerelatedlink': {
            'Meta': {'ordering': "['sort_order']", 'object_name': 'BlogIndexPageRelatedLink'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link_document': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': u"orm['wagtaildocs.Document']"}),
            'link_external': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'link_page': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': u"orm['wagtailcore.Page']"}),
            'page': ('modelcluster.fields.ParentalKey', [], {'related_name': "'related_links'", 'to': u"orm['wagtailbase.BlogIndexPage']"}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        u'wagtailbase.blogpost': {
            'Meta': {'object_name': 'BlogPost', '_ormbases': [u'wagtailbase.BaseRichTextPage']},
            u'baserichtextpage_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['wagtailbase.BaseRichTextPage']", 'unique': 'True', 'primary_key': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today'})
        },
        u'wagtailbase.blogpostrelatedlink': {
            'Meta': {'ordering': "['sort_order']", 'object_name': 'BlogPostRelatedLink'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link_document': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': u"orm['wagtaildocs.Document']"}),
            'link_external': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'link_page': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': u"orm['wagtailcore.Page']"}),
            'page': ('modelcluster.fields.ParentalKey', [], {'related_name': "'related_links'", 'to': u"orm['wagtailbase.BlogPost']"}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        u'wagtailbase.blogposttag': {
            'Meta': {'object_name': 'BlogPostTag'},
            'content_object': ('modelcluster.fields.ParentalKey', [], {'related_name': "'tagged_items'", 'to': u"orm['wagtailbase.BlogPost']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'wagtailbase_blogposttag_items'", 'to': u"orm['taggit.Tag']"})
        },
        u'wagtailbase.homepage': {
            'Meta': {'object_name': 'HomePage', '_ormbases': [u'wagtailbase.BaseRichTextPage']},
            u'baserichtextpage_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['wagtailbase.BaseRichTextPage']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'wagtailbase.indexpage': {
            'Meta': {'object_name': 'IndexPage', '_ormbases': [u'wagtailbase.BaseIndexPage']},
            u'baseindexpage_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['wagtailbase.BaseIndexPage']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'wagtailbase.indexpagerelatedlink': {
            'Meta': {'ordering': "['sort_order']", 'object_name': 'IndexPageRelatedLink'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link_document': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': u"orm['wagtaildocs.Document']"}),
            'link_external': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'link_page': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': u"orm['wagtailcore.Page']"}),
            'page': ('modelcluster.fields.ParentalKey', [], {'related_name': "'related_links'", 'to': u"orm['wagtailbase.IndexPage']"}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        u'wagtailbase.richtextpage': {
            'Meta': {'object_name': 'RichTextPage', '_ormbases': [u'wagtailbase.BaseRichTextPage']},
            u'baserichtextpage_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['wagtailbase.BaseRichTextPage']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'wagtailbase.richtextpagerelatedlink': {
            'Meta': {'ordering': "['sort_order']", 'object_name': 'RichTextPageRelatedLink'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link_document': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': u"orm['wagtaildocs.Document']"}),
            'link_external': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'link_page': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': u"orm['wagtailcore.Page']"}),
            'page': ('modelcluster.fields.ParentalKey', [], {'related_name': "'related_links'", 'to': u"orm['wagtailbase.RichTextPage']"}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        u'wagtailcore.page': {
            'Meta': {'object_name': 'Page'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'pages'", 'to': u"orm['contenttypes.ContentType']"}),
            'depth': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'has_unpublished_changes': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'live': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'numchild': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'owned_pages'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'path': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'search_description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'seo_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'show_in_menus': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'url_path': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        },
        u'wagtaildocs.document': {
            'Meta': {'object_name': 'Document'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'uploaded_by_user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['wagtailbase']