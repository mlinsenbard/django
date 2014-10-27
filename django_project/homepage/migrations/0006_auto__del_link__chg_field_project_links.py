# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Link'
        db.delete_table(u'homepage_link')


        # Renaming column for 'Project.links' to match new field type.
        db.rename_column(u'homepage_project', 'links_id', 'links')
        # Changing field 'Project.links'
        db.alter_column(u'homepage_project', 'links', self.gf('django.db.models.fields.TextField')())
        # Removing index on 'Project', fields ['links']
        db.delete_index(u'homepage_project', ['links_id'])


    def backwards(self, orm):
        # Adding index on 'Project', fields ['links']
        db.create_index(u'homepage_project', ['links_id'])

        # Adding model 'Link'
        db.create_table(u'homepage_link', (
            ('url', self.gf('django.db.models.fields.CharField')(max_length=128)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=128)),
        ))
        db.send_create_signal(u'homepage', ['Link'])


        # Renaming column for 'Project.links' to match new field type.
        db.rename_column(u'homepage_project', 'links', 'links_id')
        # Changing field 'Project.links'
        db.alter_column(u'homepage_project', 'links_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['homepage.Link']))

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
        u'homepage.project': {
            'Meta': {'object_name': 'Project'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'links': ('django.db.models.fields.TextField', [], {}),
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