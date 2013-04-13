# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'DashboardMenu'
        db.delete_table('dashboard_dashboardmenu')

        # Removing M2M table for field groups on 'DashboardMenu'
        db.delete_table('dashboard_dashboardmenu_groups')

        # Adding model 'Menu'
        db.create_table('dashboard_menu', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('data', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('memo', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('favorite', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('visible', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('parent', self.gf('mptt.fields.TreeForeignKey')(blank=True, related_name='children', null=True, to=orm['dashboard.Menu'])),
            ('lft', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('rght', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('tree_id', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('level', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
        ))
        db.send_create_signal('dashboard', ['Menu'])

        # Adding M2M table for field groups on 'Menu'
        db.create_table('dashboard_menu_groups', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('menu', models.ForeignKey(orm['dashboard.menu'], null=False)),
            ('group', models.ForeignKey(orm['auth.group'], null=False))
        ))
        db.create_unique('dashboard_menu_groups', ['menu_id', 'group_id'])


    def backwards(self, orm):
        # Adding model 'DashboardMenu'
        db.create_table('dashboard_dashboardmenu', (
            ('rght', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('parent', self.gf('mptt.fields.TreeForeignKey')(related_name='children', null=True, to=orm['dashboard.DashboardMenu'], blank=True)),
            ('memo', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('visible', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('lft', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('data', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('level', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('favorite', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('tree_id', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
        ))
        db.send_create_signal('dashboard', ['DashboardMenu'])

        # Adding M2M table for field groups on 'DashboardMenu'
        db.create_table('dashboard_dashboardmenu_groups', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('dashboardmenu', models.ForeignKey(orm['dashboard.dashboardmenu'], null=False)),
            ('group', models.ForeignKey(orm['auth.group'], null=False))
        ))
        db.create_unique('dashboard_dashboardmenu_groups', ['dashboardmenu_id', 'group_id'])

        # Deleting model 'Menu'
        db.delete_table('dashboard_menu')

        # Removing M2M table for field groups on 'Menu'
        db.delete_table('dashboard_menu_groups')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'dashboard.menu': {
            'Meta': {'ordering': "('tree_id', 'lft')", 'object_name': 'Menu'},
            'data': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'favorite': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'dashboard_menus'", 'blank': 'True', 'to': "orm['auth.Group']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'memo': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': "orm['dashboard.Menu']"}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'visible': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        }
    }

    complete_apps = ['dashboard']