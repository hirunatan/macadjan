# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'SiteInfo.proponent_email_field_enabled'
        db.add_column('macadjan_siteinfo', 'proponent_email_field_enabled', self.gf('django.db.models.fields.BooleanField')(default=True), keep_default=False)

        # Adding field 'SiteInfo.proponent_comment_field_enabled'
        db.add_column('macadjan_siteinfo', 'proponent_comment_field_enabled', self.gf('django.db.models.fields.BooleanField')(default=True), keep_default=False)

        # Adding field 'SiteInfo.alias_field_enabled'
        db.add_column('macadjan_siteinfo', 'alias_field_enabled', self.gf('django.db.models.fields.BooleanField')(default=True), keep_default=False)

        # Adding field 'SiteInfo.summary_field_enabled'
        db.add_column('macadjan_siteinfo', 'summary_field_enabled', self.gf('django.db.models.fields.BooleanField')(default=True), keep_default=False)

        # Adding field 'SiteInfo.subcategories_field_enabled'
        db.add_column('macadjan_siteinfo', 'subcategories_field_enabled', self.gf('django.db.models.fields.BooleanField')(default=True), keep_default=False)

        # Adding field 'SiteInfo.address_1_field_enabled'
        db.add_column('macadjan_siteinfo', 'address_1_field_enabled', self.gf('django.db.models.fields.BooleanField')(default=True), keep_default=False)

        # Adding field 'SiteInfo.address_2_field_enabled'
        db.add_column('macadjan_siteinfo', 'address_2_field_enabled', self.gf('django.db.models.fields.BooleanField')(default=True), keep_default=False)

        # Adding field 'SiteInfo.zipcode_field_enabled'
        db.add_column('macadjan_siteinfo', 'zipcode_field_enabled', self.gf('django.db.models.fields.BooleanField')(default=True), keep_default=False)

        # Adding field 'SiteInfo.city_field_enabled'
        db.add_column('macadjan_siteinfo', 'city_field_enabled', self.gf('django.db.models.fields.BooleanField')(default=True), keep_default=False)

        # Adding field 'SiteInfo.province_field_enabled'
        db.add_column('macadjan_siteinfo', 'province_field_enabled', self.gf('django.db.models.fields.BooleanField')(default=True), keep_default=False)

        # Adding field 'SiteInfo.country_field_enabled'
        db.add_column('macadjan_siteinfo', 'country_field_enabled', self.gf('django.db.models.fields.BooleanField')(default=True), keep_default=False)

        # Adding field 'SiteInfo.zone_field_enabled'
        db.add_column('macadjan_siteinfo', 'zone_field_enabled', self.gf('django.db.models.fields.BooleanField')(default=True), keep_default=False)

        # Adding field 'SiteInfo.latitude_field_enabled'
        db.add_column('macadjan_siteinfo', 'latitude_field_enabled', self.gf('django.db.models.fields.BooleanField')(default=True), keep_default=False)

        # Adding field 'SiteInfo.longitude_field_enabled'
        db.add_column('macadjan_siteinfo', 'longitude_field_enabled', self.gf('django.db.models.fields.BooleanField')(default=True), keep_default=False)

        # Adding field 'SiteInfo.contact_phone_1_field_enabled'
        db.add_column('macadjan_siteinfo', 'contact_phone_1_field_enabled', self.gf('django.db.models.fields.BooleanField')(default=True), keep_default=False)

        # Adding field 'SiteInfo.contact_phone_2_field_enabled'
        db.add_column('macadjan_siteinfo', 'contact_phone_2_field_enabled', self.gf('django.db.models.fields.BooleanField')(default=True), keep_default=False)

        # Adding field 'SiteInfo.fax_field_enabled'
        db.add_column('macadjan_siteinfo', 'fax_field_enabled', self.gf('django.db.models.fields.BooleanField')(default=True), keep_default=False)

        # Adding field 'SiteInfo.email_field_enabled'
        db.add_column('macadjan_siteinfo', 'email_field_enabled', self.gf('django.db.models.fields.BooleanField')(default=True), keep_default=False)

        # Adding field 'SiteInfo.email_2_field_enabled'
        db.add_column('macadjan_siteinfo', 'email_2_field_enabled', self.gf('django.db.models.fields.BooleanField')(default=True), keep_default=False)

        # Adding field 'SiteInfo.web_field_enabled'
        db.add_column('macadjan_siteinfo', 'web_field_enabled', self.gf('django.db.models.fields.BooleanField')(default=True), keep_default=False)

        # Adding field 'SiteInfo.web_2_field_enabled'
        db.add_column('macadjan_siteinfo', 'web_2_field_enabled', self.gf('django.db.models.fields.BooleanField')(default=True), keep_default=False)

        # Adding field 'SiteInfo.contact_person_field_enabled'
        db.add_column('macadjan_siteinfo', 'contact_person_field_enabled', self.gf('django.db.models.fields.BooleanField')(default=True), keep_default=False)

        # Adding field 'SiteInfo.creation_year_field_enabled'
        db.add_column('macadjan_siteinfo', 'creation_year_field_enabled', self.gf('django.db.models.fields.BooleanField')(default=True), keep_default=False)

        # Adding field 'SiteInfo.legal_form_field_enabled'
        db.add_column('macadjan_siteinfo', 'legal_form_field_enabled', self.gf('django.db.models.fields.BooleanField')(default=True), keep_default=False)

        # Adding field 'SiteInfo.description_field_enabled'
        db.add_column('macadjan_siteinfo', 'description_field_enabled', self.gf('django.db.models.fields.BooleanField')(default=True), keep_default=False)

        # Adding field 'SiteInfo.goals_field_enabled'
        db.add_column('macadjan_siteinfo', 'goals_field_enabled', self.gf('django.db.models.fields.BooleanField')(default=True), keep_default=False)

        # Adding field 'SiteInfo.finances_field_enabled'
        db.add_column('macadjan_siteinfo', 'finances_field_enabled', self.gf('django.db.models.fields.BooleanField')(default=True), keep_default=False)

        # Adding field 'SiteInfo.social_values_field_enabled'
        db.add_column('macadjan_siteinfo', 'social_values_field_enabled', self.gf('django.db.models.fields.BooleanField')(default=True), keep_default=False)

        # Adding field 'SiteInfo.how_to_access_field_enabled'
        db.add_column('macadjan_siteinfo', 'how_to_access_field_enabled', self.gf('django.db.models.fields.BooleanField')(default=True), keep_default=False)

        # Adding field 'SiteInfo.networks_member_field_enabled'
        db.add_column('macadjan_siteinfo', 'networks_member_field_enabled', self.gf('django.db.models.fields.BooleanField')(default=True), keep_default=False)

        # Adding field 'SiteInfo.networks_works_with_field_enabled'
        db.add_column('macadjan_siteinfo', 'networks_works_with_field_enabled', self.gf('django.db.models.fields.BooleanField')(default=True), keep_default=False)

        # Adding field 'SiteInfo.ongoing_projects_field_enabled'
        db.add_column('macadjan_siteinfo', 'ongoing_projects_field_enabled', self.gf('django.db.models.fields.BooleanField')(default=True), keep_default=False)

        # Adding field 'SiteInfo.needs_field_enabled'
        db.add_column('macadjan_siteinfo', 'needs_field_enabled', self.gf('django.db.models.fields.BooleanField')(default=True), keep_default=False)

        # Adding field 'SiteInfo.offerings_field_enabled'
        db.add_column('macadjan_siteinfo', 'offerings_field_enabled', self.gf('django.db.models.fields.BooleanField')(default=True), keep_default=False)

        # Adding field 'SiteInfo.additional_info_field_enabled'
        db.add_column('macadjan_siteinfo', 'additional_info_field_enabled', self.gf('django.db.models.fields.BooleanField')(default=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'SiteInfo.proponent_email_field_enabled'
        db.delete_column('macadjan_siteinfo', 'proponent_email_field_enabled')

        # Deleting field 'SiteInfo.proponent_comment_field_enabled'
        db.delete_column('macadjan_siteinfo', 'proponent_comment_field_enabled')

        # Deleting field 'SiteInfo.alias_field_enabled'
        db.delete_column('macadjan_siteinfo', 'alias_field_enabled')

        # Deleting field 'SiteInfo.summary_field_enabled'
        db.delete_column('macadjan_siteinfo', 'summary_field_enabled')

        # Deleting field 'SiteInfo.subcategories_field_enabled'
        db.delete_column('macadjan_siteinfo', 'subcategories_field_enabled')

        # Deleting field 'SiteInfo.address_1_field_enabled'
        db.delete_column('macadjan_siteinfo', 'address_1_field_enabled')

        # Deleting field 'SiteInfo.address_2_field_enabled'
        db.delete_column('macadjan_siteinfo', 'address_2_field_enabled')

        # Deleting field 'SiteInfo.zipcode_field_enabled'
        db.delete_column('macadjan_siteinfo', 'zipcode_field_enabled')

        # Deleting field 'SiteInfo.city_field_enabled'
        db.delete_column('macadjan_siteinfo', 'city_field_enabled')

        # Deleting field 'SiteInfo.province_field_enabled'
        db.delete_column('macadjan_siteinfo', 'province_field_enabled')

        # Deleting field 'SiteInfo.country_field_enabled'
        db.delete_column('macadjan_siteinfo', 'country_field_enabled')

        # Deleting field 'SiteInfo.zone_field_enabled'
        db.delete_column('macadjan_siteinfo', 'zone_field_enabled')

        # Deleting field 'SiteInfo.latitude_field_enabled'
        db.delete_column('macadjan_siteinfo', 'latitude_field_enabled')

        # Deleting field 'SiteInfo.longitude_field_enabled'
        db.delete_column('macadjan_siteinfo', 'longitude_field_enabled')

        # Deleting field 'SiteInfo.contact_phone_1_field_enabled'
        db.delete_column('macadjan_siteinfo', 'contact_phone_1_field_enabled')

        # Deleting field 'SiteInfo.contact_phone_2_field_enabled'
        db.delete_column('macadjan_siteinfo', 'contact_phone_2_field_enabled')

        # Deleting field 'SiteInfo.fax_field_enabled'
        db.delete_column('macadjan_siteinfo', 'fax_field_enabled')

        # Deleting field 'SiteInfo.email_field_enabled'
        db.delete_column('macadjan_siteinfo', 'email_field_enabled')

        # Deleting field 'SiteInfo.email_2_field_enabled'
        db.delete_column('macadjan_siteinfo', 'email_2_field_enabled')

        # Deleting field 'SiteInfo.web_field_enabled'
        db.delete_column('macadjan_siteinfo', 'web_field_enabled')

        # Deleting field 'SiteInfo.web_2_field_enabled'
        db.delete_column('macadjan_siteinfo', 'web_2_field_enabled')

        # Deleting field 'SiteInfo.contact_person_field_enabled'
        db.delete_column('macadjan_siteinfo', 'contact_person_field_enabled')

        # Deleting field 'SiteInfo.creation_year_field_enabled'
        db.delete_column('macadjan_siteinfo', 'creation_year_field_enabled')

        # Deleting field 'SiteInfo.legal_form_field_enabled'
        db.delete_column('macadjan_siteinfo', 'legal_form_field_enabled')

        # Deleting field 'SiteInfo.description_field_enabled'
        db.delete_column('macadjan_siteinfo', 'description_field_enabled')

        # Deleting field 'SiteInfo.goals_field_enabled'
        db.delete_column('macadjan_siteinfo', 'goals_field_enabled')

        # Deleting field 'SiteInfo.finances_field_enabled'
        db.delete_column('macadjan_siteinfo', 'finances_field_enabled')

        # Deleting field 'SiteInfo.social_values_field_enabled'
        db.delete_column('macadjan_siteinfo', 'social_values_field_enabled')

        # Deleting field 'SiteInfo.how_to_access_field_enabled'
        db.delete_column('macadjan_siteinfo', 'how_to_access_field_enabled')

        # Deleting field 'SiteInfo.networks_member_field_enabled'
        db.delete_column('macadjan_siteinfo', 'networks_member_field_enabled')

        # Deleting field 'SiteInfo.networks_works_with_field_enabled'
        db.delete_column('macadjan_siteinfo', 'networks_works_with_field_enabled')

        # Deleting field 'SiteInfo.ongoing_projects_field_enabled'
        db.delete_column('macadjan_siteinfo', 'ongoing_projects_field_enabled')

        # Deleting field 'SiteInfo.needs_field_enabled'
        db.delete_column('macadjan_siteinfo', 'needs_field_enabled')

        # Deleting field 'SiteInfo.offerings_field_enabled'
        db.delete_column('macadjan_siteinfo', 'offerings_field_enabled')

        # Deleting field 'SiteInfo.additional_info_field_enabled'
        db.delete_column('macadjan_siteinfo', 'additional_info_field_enabled')


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
            'additional_info_field_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'additional_info_hints': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'address_1_field_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'address_2_field_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'alias_field_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'change_proposal_text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'change_proposal_title': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'city_field_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'contact_person_field_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'contact_phone_1_field_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'contact_phone_2_field_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'country_field_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'creation_year_field_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'description_field_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'description_hints': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'email_2_field_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'email_field_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'entity_change_proposal_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'fax_field_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'finances_field_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'finances_hints': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'footer_line': ('django.db.models.fields.TextField', [], {}),
            'goals_field_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'goals_hints': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'how_to_access_field_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'how_to_access_hints': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude_field_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'legal_form_field_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'longitude_field_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
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
            'needs_field_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'needs_hints': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'networks_member_field_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'networks_member_hints': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'networks_works_with_field_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'networks_works_with_hints': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'new_entity_proposal_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'new_entity_proposal_text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'new_entity_proposal_title': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'offerings_field_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'offerings_hints': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'ongoing_projects_field_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'ongoing_projects_hints': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'proponent_comment_field_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'proponent_email_field_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'proposal_bottom_text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'province_field_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'site': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'site_info'", 'unique': 'True', 'to': "orm['sites.Site']"}),
            'social_values_field_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'social_values_hints': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'subcategories_field_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'summary_field_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'web_2_field_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'web_field_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'website_description': ('django.db.models.fields.TextField', [], {}),
            'website_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'website_subtitle': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'blank': 'True'}),
            'zipcode_field_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'zone_field_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
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
