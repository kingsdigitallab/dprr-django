# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Praenomen'
        db.create_table(u'promrep_praenomen', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('abbrev', self.gf('django.db.models.fields.CharField')(unique=True, max_length=32)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=128)),
        ))
        db.send_create_signal(u'promrep', ['Praenomen'])

        # Adding model 'Sex'
        db.create_table(u'promrep_sex', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=64)),
        ))
        db.send_create_signal(u'promrep', ['Sex'])

        # Adding model 'RoleType'
        db.create_table(u'promrep_roletype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=128)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=1024, blank=True)),
        ))
        db.send_create_signal(u'promrep', ['RoleType'])

        # Adding model 'Certainty'
        db.create_table(u'promrep_certainty', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=64)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=256, blank=True)),
        ))
        db.send_create_signal(u'promrep', ['Certainty'])

        # Adding model 'Person'
        db.create_table(u'promrep_person', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            ('original_text', self.gf('django.db.models.fields.CharField')(max_length=256, blank=True)),
            ('praenomen', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['promrep.Praenomen'], null=True, blank=True)),
            ('nomen', self.gf('django.db.models.fields.CharField')(max_length=128, blank=True)),
            ('cognomen_first', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
            ('cognomen_other', self.gf('django.db.models.fields.CharField')(max_length=128, blank=True)),
            ('sex', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['promrep.Sex'], null=True, blank=True)),
            ('tribe', self.gf('django.db.models.fields.CharField')(max_length=128, blank=True)),
            ('is_patrician', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('patrician_certainty', self.gf('django.db.models.fields.related.ForeignKey')(related_name='person_patrician_certainty', to=orm['promrep.Certainty'])),
            ('is_noble', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('noble_certainty', self.gf('django.db.models.fields.related.ForeignKey')(related_name='person_noble_certainty', to=orm['promrep.Certainty'])),
            ('is_novus_homo', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('novus_homo_certainty', self.gf('django.db.models.fields.related.ForeignKey')(related_name='person_novus_homo_certainty', to=orm['promrep.Certainty'])),
            ('notes', self.gf('django.db.models.fields.CharField')(max_length=1024, blank=True)),
            ('filliation', self.gf('django.db.models.fields.CharField')(max_length=256, blank=True)),
            ('real_number', self.gf('django.db.models.fields.CharField')(max_length=32, blank=True)),
            ('real_number_old', self.gf('django.db.models.fields.CharField')(max_length=32, blank=True)),
            ('real_attribute', self.gf('django.db.models.fields.CharField')(max_length=128, blank=True)),
        ))
        db.send_create_signal(u'promrep', ['Person'])

        # Adding model 'SecondarySource'
        db.create_table(u'promrep_secondarysource', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=256)),
            ('abbrev_name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=256, blank=True)),
            ('biblio', self.gf('django.db.models.fields.CharField')(unique=True, max_length=512, blank=True)),
        ))
        db.send_create_signal(u'promrep', ['SecondarySource'])

        # Adding model 'PrimarySource'
        db.create_table(u'promrep_primarysource', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=256)),
        ))
        db.send_create_signal(u'promrep', ['PrimarySource'])

        # Adding model 'Office'
        db.create_table(u'promrep_office', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=256)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=1024, blank=True)),
            ('parent', self.gf('mptt.fields.TreeForeignKey')(blank=True, related_name='children', null=True, to=orm['promrep.Office'])),
            (u'lft', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            (u'rght', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            (u'tree_id', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            (u'level', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
        ))
        db.send_create_signal(u'promrep', ['Office'])

        # Adding model 'AssertionType'
        db.create_table(u'promrep_assertiontype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=128)),
        ))
        db.send_create_signal(u'promrep', ['AssertionType'])

        # Adding model 'Assertion'
        db.create_table(u'promrep_assertion', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            ('assertion_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['promrep.AssertionType'])),
            ('office', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['promrep.Office'])),
            ('secondary_source', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['promrep.SecondarySource'])),
            ('display_text', self.gf('django.db.models.fields.CharField')(max_length=1024, blank=True)),
            ('date_year', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
            ('notes', self.gf('django.db.models.fields.CharField')(max_length=1024, blank=True)),
        ))
        db.send_create_signal(u'promrep', ['Assertion'])

        # Adding model 'AssertionPerson'
        db.create_table(u'promrep_assertionperson', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['promrep.Person'])),
            ('assertion', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['promrep.Assertion'])),
            ('role', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['promrep.RoleType'])),
            ('original_text', self.gf('django.db.models.fields.CharField')(max_length=1024, blank=True)),
        ))
        db.send_create_signal(u'promrep', ['AssertionPerson'])

        # Adding model 'DateType'
        db.create_table(u'promrep_datetype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'promrep', ['DateType'])

        # Adding model 'Date'
        db.create_table(u'promrep_date', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('date_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['promrep.DateType'], null=True, blank=True)),
            ('interval', self.gf('django.db.models.fields.SmallIntegerField')()),
            ('year', self.gf('promrep.models.IntegerRangeField')(null=True, blank=True)),
            ('year_uncertain', self.gf('django.db.models.fields.BooleanField')()),
            ('month', self.gf('promrep.models.IntegerRangeField')(null=True, blank=True)),
            ('month_uncertain', self.gf('django.db.models.fields.BooleanField')()),
            ('day', self.gf('promrep.models.IntegerRangeField')(null=True, blank=True)),
            ('day_uncertain', self.gf('django.db.models.fields.BooleanField')()),
            ('circa', self.gf('django.db.models.fields.BooleanField')()),
            ('notes', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'promrep', ['Date'])


    def backwards(self, orm):
        # Deleting model 'Praenomen'
        db.delete_table(u'promrep_praenomen')

        # Deleting model 'Sex'
        db.delete_table(u'promrep_sex')

        # Deleting model 'RoleType'
        db.delete_table(u'promrep_roletype')

        # Deleting model 'Certainty'
        db.delete_table(u'promrep_certainty')

        # Deleting model 'Person'
        db.delete_table(u'promrep_person')

        # Deleting model 'SecondarySource'
        db.delete_table(u'promrep_secondarysource')

        # Deleting model 'PrimarySource'
        db.delete_table(u'promrep_primarysource')

        # Deleting model 'Office'
        db.delete_table(u'promrep_office')

        # Deleting model 'AssertionType'
        db.delete_table(u'promrep_assertiontype')

        # Deleting model 'Assertion'
        db.delete_table(u'promrep_assertion')

        # Deleting model 'AssertionPerson'
        db.delete_table(u'promrep_assertionperson')

        # Deleting model 'DateType'
        db.delete_table(u'promrep_datetype')

        # Deleting model 'Date'
        db.delete_table(u'promrep_date')


    models = {
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'promrep.assertion': {
            'Meta': {'object_name': 'Assertion'},
            'assertion_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['promrep.AssertionType']"}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'date_year': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'display_text': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'notes': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'blank': 'True'}),
            'office': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['promrep.Office']"}),
            'persons': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['promrep.Person']", 'through': u"orm['promrep.AssertionPerson']", 'symmetrical': 'False'}),
            'secondary_source': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['promrep.SecondarySource']"})
        },
        u'promrep.assertionperson': {
            'Meta': {'object_name': 'AssertionPerson'},
            'assertion': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['promrep.Assertion']"}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'original_text': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'blank': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['promrep.Person']"}),
            'role': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['promrep.RoleType']"})
        },
        u'promrep.assertiontype': {
            'Meta': {'object_name': 'AssertionType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'})
        },
        u'promrep.certainty': {
            'Meta': {'object_name': 'Certainty'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'})
        },
        u'promrep.date': {
            'Meta': {'object_name': 'Date'},
            'circa': ('django.db.models.fields.BooleanField', [], {}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['promrep.DateType']", 'null': 'True', 'blank': 'True'}),
            'day': ('promrep.models.IntegerRangeField', [], {'null': 'True', 'blank': 'True'}),
            'day_uncertain': ('django.db.models.fields.BooleanField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interval': ('django.db.models.fields.SmallIntegerField', [], {}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'month': ('promrep.models.IntegerRangeField', [], {'null': 'True', 'blank': 'True'}),
            'month_uncertain': ('django.db.models.fields.BooleanField', [], {}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'year': ('promrep.models.IntegerRangeField', [], {'null': 'True', 'blank': 'True'}),
            'year_uncertain': ('django.db.models.fields.BooleanField', [], {})
        },
        u'promrep.datetype': {
            'Meta': {'ordering': "['name']", 'object_name': 'DateType'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        },
        u'promrep.office': {
            'Meta': {'ordering': "['tree_id', 'lft', 'name']", 'object_name': 'Office'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            u'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            u'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '256'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': u"orm['promrep.Office']"}),
            u'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            u'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        u'promrep.person': {
            'Meta': {'object_name': 'Person'},
            'cognomen_first': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'cognomen_other': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'filliation': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_noble': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_novus_homo': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_patrician': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'noble_certainty': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'person_noble_certainty'", 'to': u"orm['promrep.Certainty']"}),
            'nomen': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'notes': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'blank': 'True'}),
            'novus_homo_certainty': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'person_novus_homo_certainty'", 'to': u"orm['promrep.Certainty']"}),
            'original_text': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'patrician_certainty': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'person_patrician_certainty'", 'to': u"orm['promrep.Certainty']"}),
            'praenomen': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['promrep.Praenomen']", 'null': 'True', 'blank': 'True'}),
            'real_attribute': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'real_number': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'real_number_old': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'sex': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['promrep.Sex']", 'null': 'True', 'blank': 'True'}),
            'tribe': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'})
        },
        u'promrep.praenomen': {
            'Meta': {'ordering': "['name']", 'object_name': 'Praenomen'},
            'abbrev': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'})
        },
        u'promrep.primarysource': {
            'Meta': {'object_name': 'PrimarySource'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '256'})
        },
        u'promrep.roletype': {
            'Meta': {'object_name': 'RoleType'},
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'})
        },
        u'promrep.secondarysource': {
            'Meta': {'object_name': 'SecondarySource'},
            'abbrev_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '256', 'blank': 'True'}),
            'biblio': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '512', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '256'})
        },
        u'promrep.sex': {
            'Meta': {'object_name': 'Sex'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'})
        }
    }

    complete_apps = ['promrep']