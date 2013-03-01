# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'SiteInfo.new_entity_proposal_title'
        db.add_column('macadjan_siteinfo', 'new_entity_proposal_title', self.gf('django.db.models.fields.CharField')(default='', max_length=100, blank=True), keep_default=False)

        # Adding field 'SiteInfo.new_entity_proposal_text'
        db.add_column('macadjan_siteinfo', 'new_entity_proposal_text', self.gf('django.db.models.fields.TextField')(default='', blank=True), keep_default=False)

        # Adding field 'SiteInfo.change_proposal_title'
        db.add_column('macadjan_siteinfo', 'change_proposal_title', self.gf('django.db.models.fields.CharField')(default='', max_length=100, blank=True), keep_default=False)

        # Adding field 'SiteInfo.change_proposal_text'
        db.add_column('macadjan_siteinfo', 'change_proposal_text', self.gf('django.db.models.fields.TextField')(default='', blank=True), keep_default=False)

        # Adding field 'SiteInfo.proposal_bottom_text'
        db.add_column('macadjan_siteinfo', 'proposal_bottom_text', self.gf('django.db.models.fields.TextField')(default='', blank=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'SiteInfo.new_entity_proposal_title'
        db.delete_column('macadjan_siteinfo', 'new_entity_proposal_title')

        # Deleting field 'SiteInfo.new_entity_proposal_text'
        db.delete_column('macadjan_siteinfo', 'new_entity_proposal_text')

        # Deleting field 'SiteInfo.change_proposal_title'
        db.delete_column('macadjan_siteinfo', 'change_proposal_title')

        # Deleting field 'SiteInfo.change_proposal_text'
        db.delete_column('macadjan_siteinfo', 'change_proposal_text')

        # Deleting field 'SiteInfo.proposal_bottom_text'
        db.delete_column('macadjan_siteinfo', 'proposal_bottom_text')


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
            'change_proposal_text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'change_proposal_title': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
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
            'new_entity_proposal_text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'new_entity_proposal_title': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'offerings_hints': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'ongoing_projects_hints': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'proposal_bottom_text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
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
