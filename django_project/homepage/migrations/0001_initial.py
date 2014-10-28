# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Tag'
        db.create_table(u'homepage_tag', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=64)),
        ))
        db.send_create_signal(u'homepage', ['Tag'])

        # Adding model 'BlogEntry'
        db.create_table(u'homepage_blogentry', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('subtitle', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('picture', self.gf('django.db.models.fields.CharField')(max_length=128, blank=True)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'homepage', ['BlogEntry'])

        # Adding M2M table for field tags on 'BlogEntry'
        db.create_table(u'homepage_blogentry_tags', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('blogentry', models.ForeignKey(orm[u'homepage.blogentry'], null=False)),
            ('tag', models.ForeignKey(orm[u'homepage.tag'], null=False))
        ))
        db.create_unique(u'homepage_blogentry_tags', ['blogentry_id', 'tag_id'])

        # Adding model 'Project'
        db.create_table(u'homepage_project', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('picture', self.gf('django.db.models.fields.CharField')(max_length=128, blank=True)),
            ('links', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'homepage', ['Project'])


    def backwards(self, orm):
        # Deleting model 'Tag'
        db.delete_table(u'homepage_tag')

        # Deleting model 'BlogEntry'
        db.delete_table(u'homepage_blogentry')

        # Removing M2M table for field tags on 'BlogEntry'
        db.delete_table('homepage_blogentry_tags')

        # Deleting model 'Project'
        db.delete_table(u'homepage_project')


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
            'picture': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        u'homepage.tag': {
            'Meta': {'object_name': 'Tag'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        }
    }

    complete_apps = ['homepage']