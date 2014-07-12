# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Category'
        db.create_table(u'edges_category', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal(u'edges', ['Category'])

        # Adding model 'Requirements'
        db.create_table(u'edges_requirements', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('edge', self.gf('django.db.models.fields.related.ForeignKey')(related_name='requirements', to=orm['edges.Edge'])),
        ))
        db.send_create_signal(u'edges', ['Requirements'])

        # Adding model 'Edge'
        db.create_table(u'edges_edge', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['edges.Category'])),
        ))
        db.send_create_signal(u'edges', ['Edge'])


    def backwards(self, orm):
        # Deleting model 'Category'
        db.delete_table(u'edges_category')

        # Deleting model 'Requirements'
        db.delete_table(u'edges_requirements')

        # Deleting model 'Edge'
        db.delete_table(u'edges_edge')


    models = {
        u'edges.category': {
            'Meta': {'object_name': 'Category'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        u'edges.edge': {
            'Meta': {'object_name': 'Edge'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['edges.Category']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        u'edges.requirements': {
            'Meta': {'object_name': 'Requirements'},
            'edge': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'requirements'", 'to': u"orm['edges.Edge']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        }
    }

    complete_apps = ['edges']