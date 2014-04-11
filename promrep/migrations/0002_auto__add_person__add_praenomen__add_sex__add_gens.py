# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Person'
        db.create_table(u'promrep_person', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            ('praenomen', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['promrep.Praenomen'])),
            ('nomen', self.gf('django.db.models.fields.CharField')(unique=True, max_length=128)),
            ('cognomen', self.gf('django.db.models.fields.CharField')(unique=True, max_length=128)),
            ('sex', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['promrep.Sex'])),
            ('gens', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['promrep.Gens'])),
            ('real_number', self.gf('django.db.models.fields.CharField')(unique=True, max_length=32)),
            ('real_attribute', self.gf('django.db.models.fields.CharField')(unique=True, max_length=128)),
        ))
        db.send_create_signal(u'promrep', ['Person'])

        # Adding model 'Praenomen'
        db.create_table(u'promrep_praenomen', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('abbrev', self.gf('django.db.models.fields.CharField')(unique=True, max_length=32)),
            ('male_form', self.gf('django.db.models.fields.CharField')(unique=True, max_length=128)),
            ('female_name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=128)),
        ))
        db.send_create_signal(u'promrep', ['Praenomen'])

        # Adding model 'Sex'
        db.create_table(u'promrep_sex', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=32)),
        ))
        db.send_create_signal(u'promrep', ['Sex'])

        # Adding model 'Gens'
        db.create_table(u'promrep_gens', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=128)),
        ))
        db.send_create_signal(u'promrep', ['Gens'])


    def backwards(self, orm):
        # Deleting model 'Person'
        db.delete_table(u'promrep_person')

        # Deleting model 'Praenomen'
        db.delete_table(u'promrep_praenomen')

        # Deleting model 'Sex'
        db.delete_table(u'promrep_sex')

        # Deleting model 'Gens'
        db.delete_table(u'promrep_gens')


    models = {
        u'promrep.gens': {
            'Meta': {'object_name': 'Gens'},
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'})
        },
        u'promrep.person': {
            'Meta': {'object_name': 'Person'},
            'cognomen': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'gens': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['promrep.Gens']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'nomen': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'}),
            'praenomen': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['promrep.Praenomen']"}),
            'real_attribute': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'}),
            'real_number': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32'}),
            'sex': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['promrep.Sex']"})
        },
        u'promrep.praenomen': {
            'Meta': {'object_name': 'Praenomen'},
            'abbrev': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32'}),
            'female_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'male_form': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'})
        },
        u'promrep.sex': {
            'Meta': {'object_name': 'Sex'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32'})
        }
    }

    complete_apps = ['promrep']