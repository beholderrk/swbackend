# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Requirements.mode'
        db.add_column(u'edges_requirements', 'mode',
                      self.gf('django.db.models.fields.CharField')(default='rank', max_length=30),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Requirements.mode'
        db.delete_column(u'edges_requirements', 'mode')


    models = {
        u'edges.category': {
            'Meta': {'object_name': 'Category'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        u'edges.edge': {
            'Meta': {'object_name': 'Edge'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['edges.Category']"}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        u'edges.requirements': {
            'Meta': {'object_name': 'Requirements'},
            'edge': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'requirements'", 'to': u"orm['edges.Edge']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mode': ('django.db.models.fields.CharField', [], {'default': "'rank'", 'max_length': '30'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        }
    }

    complete_apps = ['edges']