# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'SiteInfo'
        db.create_table('macadjan_siteinfo', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('site', self.gf('django.db.models.fields.related.OneToOneField')(related_name='site_info', unique=True, to=orm['sites.Site'])),
            ('website_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('website_subtitle', self.gf('django.db.models.fields.CharField')(default='', max_length=100, blank=True)),
            ('website_description', self.gf('django.db.models.fields.TextField')()),
            ('footer_line', self.gf('django.db.models.fields.TextField')()),
            ('map_bounds_left', self.gf('django.db.models.fields.FloatField')(default=-20037508.34)),
            ('map_bounds_right', self.gf('django.db.models.fields.FloatField')(default=20037508.34)),
            ('map_bounds_bottom', self.gf('django.db.models.fields.FloatField')(default=-20037508.34)),
            ('map_bounds_top', self.gf('django.db.models.fields.FloatField')(default=20037508.34)),
            ('map_zoom_levels', self.gf('django.db.models.fields.IntegerField')(default=18)),
            ('map_max_resolution', self.gf('django.db.models.fields.IntegerField')(default=156543)),
            ('map_units', self.gf('django.db.models.fields.CharField')(default='meters', max_length=50)),
            ('map_initial_lon', self.gf('django.db.models.fields.FloatField')()),
            ('map_initial_lat', self.gf('django.db.models.fields.FloatField')()),
            ('map_initial_zoom', self.gf('django.db.models.fields.IntegerField')()),
            ('new_entity_proposal_enabled', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('entity_change_proposal_enabled', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('description_hints', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('goals_hints', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('finances_hints', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('social_values_hints', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('how_to_access_hints', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('networks_member_hints', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('networks_works_with_hints', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('ongoing_projects_hints', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('needs_hints', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('offerings_hints', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('additional_info_hints', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
        ))
        db.send_create_signal('macadjan', ['SiteInfo'])

        # Adding model 'EntityType'
        db.create_table('macadjan_entitytype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('macadjan', ['EntityType'])

        # Adding model 'Category'
        db.create_table('macadjan_category', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=100, db_index=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('marker_url', self.gf('django.db.models.fields.CharField')(default='', max_length=100, blank=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('macadjan', ['Category'])

        # Adding model 'SubCategory'
        db.create_table('macadjan_subcategory', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(related_name='subcategories', to=orm['macadjan.Category'])),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=100, db_index=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('marker_url', self.gf('django.db.models.fields.CharField')(default='', max_length=100, blank=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('macadjan', ['SubCategory'])

        # Adding model 'TagCollection'
        db.create_table('macadjan_tagcollection', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=100, db_index=True)),
        ))
        db.send_create_signal('macadjan', ['TagCollection'])

        # Adding model 'EntityTag'
        db.create_table('macadjan_entitytag', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=100, db_index=True)),
            ('collection', self.gf('django.db.models.fields.related.ForeignKey')(related_name='tags', to=orm['macadjan.TagCollection'])),
        ))
        db.send_create_signal('macadjan', ['EntityTag'])


    def backwards(self, orm):
        
        # Deleting model 'SiteInfo'
        db.delete_table('macadjan_siteinfo')

        # Deleting model 'EntityType'
        db.delete_table('macadjan_entitytype')

        # Deleting model 'Category'
        db.delete_table('macadjan_category')

        # Deleting model 'SubCategory'
        db.delete_table('macadjan_subcategory')

        # Deleting model 'TagCollection'
        db.delete_table('macadjan_tagcollection')

        # Deleting model 'EntityTag'
        db.delete_table('macadjan_entitytag')


    models = {
        'macadjan.category': {
            'Meta': {'ordering': "['name']", 'object_name': 'Category'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'marker_url': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100', 'db_index': 'True'})
        },
        'macadjan.entitytag': {
            'Meta': {'ordering': "['collection', 'name']", 'object_name': 'EntityTag'},
            'collection': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'tags'", 'to': "orm['macadjan.TagCollection']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100', 'db_index': 'True'})
        },
        'macadjan.entitytype': {
            'Meta': {'ordering': "['name']", 'object_name': 'EntityType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'macadjan.siteinfo': {
            'Meta': {'ordering': "['website_name']", 'object_name': 'SiteInfo'},
            'additional_info_hints': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'description_hints': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'entity_change_proposal_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'finances_hints': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'footer_line': ('django.db.models.fields.TextField', [], {}),
            'goals_hints': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'how_to_access_hints': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'map_bounds_bottom': ('django.db.models.fields.FloatField', [], {'default': '-20037508.34'}),
            'map_bounds_left': ('django.db.models.fields.FloatField', [], {'default': '-20037508.34'}),
            'map_bounds_right': ('django.db.models.fields.FloatField', [], {'default': '20037508.34'}),
            'map_bounds_top': ('django.db.models.fields.FloatField', [], {'default': '20037508.34'}),
            'map_initial_lat': ('django.db.models.fields.FloatField', [], {}),
            'map_initial_lon': ('django.db.models.fields.FloatField', [], {}),
            'map_initial_zoom': ('django.db.models.fields.IntegerField', [], {}),
            'map_max_resolution': ('django.db.models.fields.IntegerField', [], {'default': '156543'}),
            'map_units': ('django.db.models.fields.CharField', [], {'default': "'meters'", 'max_length': '50'}),
            'map_zoom_levels': ('django.db.models.fields.IntegerField', [], {'default': '18'}),
            'needs_hints': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'networks_member_hints': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'networks_works_with_hints': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'new_entity_proposal_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'offerings_hints': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'ongoing_projects_hints': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'site': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'site_info'", 'unique': 'True', 'to': "orm['sites.Site']"}),
            'social_values_hints': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'website_description': ('django.db.models.fields.TextField', [], {}),
            'website_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'website_subtitle': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'blank': 'True'})
        },
        'macadjan.subcategory': {
            'Meta': {'ordering': "['category', 'name']", 'object_name': 'SubCategory'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'subcategories'", 'to': "orm['macadjan.Category']"}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'marker_url': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100', 'db_index': 'True'})
        },
        'macadjan.tagcollection': {
            'Meta': {'ordering': "['name']", 'object_name': 'TagCollection'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100', 'db_index': 'True'})
        },
        'sites.site': {
            'Meta': {'ordering': "('domain',)", 'object_name': 'Site', 'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['macadjan']
