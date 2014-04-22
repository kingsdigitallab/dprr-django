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
            ('description', self.gf('django.db.models.fields.CharField')(unique=True, max_length=1024)),
        ))
        db.send_create_signal(u'promrep', ['RoleType'])

        # Adding model 'Person'
        db.create_table(u'promrep_person', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            ('praenomen', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['promrep.Praenomen'])),
            ('nomen', self.gf('django.db.models.fields.CharField')(unique=True, max_length=128)),
            ('cognomen', self.gf('django.db.models.fields.CharField')(unique=True, max_length=128)),
            ('sex', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['promrep.Sex'])),
            ('real_number', self.gf('django.db.models.fields.CharField')(unique=True, max_length=32)),
            ('real_attribute', self.gf('django.db.models.fields.CharField')(unique=True, max_length=128)),
        ))
        db.send_create_signal(u'promrep', ['Person'])

        # Adding model 'Office'
        db.create_table(u'promrep_office', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=256)),
            ('description', self.gf('django.db.models.fields.CharField')(unique=True, max_length=1024)),
            ('notes', self.gf('django.db.models.fields.CharField')(unique=True, max_length=1024)),
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
            ('display_text', self.gf('django.db.models.fields.CharField')(unique=True, max_length=1024)),
            ('date_year', self.gf('django.db.models.fields.CharField')(unique=True, max_length=64)),
            ('notes', self.gf('django.db.models.fields.CharField')(unique=True, max_length=1024)),
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
            ('original_text', self.gf('django.db.models.fields.CharField')(unique=True, max_length=1024)),
        ))
        db.send_create_signal(u'promrep', ['AssertionPerson'])


    def backwards(self, orm):
        # Deleting model 'Praenomen'
        db.delete_table(u'promrep_praenomen')

        # Deleting model 'Sex'
        db.delete_table(u'promrep_sex')

        # Deleting model 'RoleType'
        db.delete_table(u'promrep_roletype')

        # Deleting model 'Person'
        db.delete_table(u'promrep_person')

        # Deleting model 'Office'
        db.delete_table(u'promrep_office')

        # Deleting model 'AssertionType'
        db.delete_table(u'promrep_assertiontype')

        # Deleting model 'Assertion'
        db.delete_table(u'promrep_assertion')

        # Deleting model 'AssertionPerson'
        db.delete_table(u'promrep_assertionperson')


    models = {
        u'promrep.assertion': {
            'Meta': {'object_name': 'Assertion'},
            'assertion_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['promrep.AssertionType']"}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'date_year': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'}),
            'display_text': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '1024'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'notes': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '1024'}),
            'persons': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['promrep.Person']", 'through': u"orm['promrep.AssertionPerson']", 'symmetrical': 'False'})
        },
        u'promrep.assertionperson': {
            'Meta': {'object_name': 'AssertionPerson'},
            'assertion': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['promrep.Assertion']"}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'original_text': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '1024'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['promrep.Person']"}),
            'role': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['promrep.RoleType']"})
        },
        u'promrep.assertiontype': {
            'Meta': {'object_name': 'AssertionType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'})
        },
        u'promrep.office': {
            'Meta': {'object_name': 'Office'},
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'description': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '1024'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '256'}),
            'notes': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '1024'})
        },
        u'promrep.person': {
            'Meta': {'object_name': 'Person'},
            'cognomen': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'nomen': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'}),
            'praenomen': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['promrep.Praenomen']"}),
            'real_attribute': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'}),
            'real_number': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32'}),
            'sex': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['promrep.Sex']"})
        },
        u'promrep.praenomen': {
            'Meta': {'ordering': "['name']", 'object_name': 'Praenomen'},
            'abbrev': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'})
        },
        u'promrep.roletype': {
            'Meta': {'object_name': 'RoleType'},
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'description': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '1024'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'})
        },
        u'promrep.sex': {
            'Meta': {'object_name': 'Sex'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'})
        }
    }

    complete_apps = ['promrep']