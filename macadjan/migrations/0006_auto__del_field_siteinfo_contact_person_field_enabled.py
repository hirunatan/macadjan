# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'SiteInfo.contact_person_field_enabled'
        db.delete_column(u'macadjan_siteinfo', 'contact_person_field_enabled')


    def backwards(self, orm):
        # Adding field 'SiteInfo.contact_person_field_enabled'
        db.add_column(u'macadjan_siteinfo', 'contact_person_field_enabled',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'macadjan.category': {
            'Meta': {'ordering': "['name']", 'object_name': 'Category'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'marker_url': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100'})
        },
        u'macadjan.entitytag': {
            'Meta': {'ordering': "['collection', 'name']", 'object_name': 'EntityTag'},
            'collection': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'tags'", 'to': u"orm['macadjan.TagCollection']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100'})
        },
        u'macadjan.entitytype': {
            'Meta': {'ordering': "['name']", 'object_name': 'EntityType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'macadjan.macadjanuserprofile': {
            'Meta': {'ordering': "['user']", 'object_name': 'MacadjanUserProfile'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'map_source': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'user_profiles'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['macadjan.MapSource']"}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'macadjan_profile'", 'unique': 'True', 'to': u"orm['auth.User']"})
        },
        u'macadjan.mapsource': {
            'Meta': {'ordering': "['name']", 'object_name': 'MapSource'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100', 'blank': 'True'}),
            'web': ('django.db.models.fields.URLField', [], {'default': "''", 'max_length': '200', 'blank': 'True'})
        },
        u'macadjan.siteinfo': {
            'Meta': {'ordering': "['website_name']", 'object_name': 'SiteInfo'},
            'additional_info_field_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'additional_info_hints': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'address_1_field_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'address_2_field_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'alias_field_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'change_proposal_text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'change_proposal_title': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'city_field_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
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
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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
            'site': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'site_info'", 'unique': 'True', 'to': u"orm['sites.Site']"}),
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
        u'macadjan.subcategory': {
            'Meta': {'ordering': "['category', 'name']", 'object_name': 'SubCategory'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'subcategories'", 'to': u"orm['macadjan.Category']"}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'marker_url': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100'})
        },
        u'macadjan.tagcollection': {
            'Meta': {'ordering': "['name']", 'object_name': 'TagCollection'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100'})
        },
        u'sites.site': {
            'Meta': {'ordering': "('domain',)", 'object_name': 'Site', 'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['macadjan']