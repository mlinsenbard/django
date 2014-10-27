# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'BlogEntry.picture'
        db.alter_column(u'homepage_blogentry', 'picture', self.gf('django.db.models.fields.CharField')(max_length=128))

    def backwards(self, orm):

        # Changing field 'BlogEntry.picture'
        db.alter_column(u'homepage_blogentry', 'picture', self.gf('django.db.models.fields.CharField')(max_length=32))

    models = {
        u'homepage.blogentry': {
            'Meta': {'object_name': 'BlogEntry'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'picture': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'subtitle': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['homepage.Tag']", 'symmetrical': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        u'homepage.link': {
            'Meta': {'object_name': 'Link'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        u'homepage.project': {
            'Meta': {'object_name': 'Project'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'links': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['homepage.Link']"}),
            'picture': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        u'homepage.tag': {
            'Meta': {'object_name': 'Tag'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        }
    }

    complete_apps = ['homepage']