# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.sites.models import Site
from django.db.models import signals
from django.conf import settings
from django.template import RequestContext, Context, loader

from .utils import slugify_uniquely

from haystack.query import SearchQuerySet
from datetime import datetime


class SiteInfo(models.Model):
    '''
    General info of the website.
    '''
    # Link to the site that this SiteInfo apply
    site = models.OneToOneField(Site, related_name = 'site_info',
            verbose_name = _(u'Sitio'),
            help_text = _(u'Dominio al que se aplica esta info.'))

    # Website data
    website_name = models.CharField(max_length = 100, null = False, blank = False,
            verbose_name = _(u'Nombre del sitio'),
            help_text = _(u'Nombre global del sitio, aparece en la parte superior de todas las páginas.'))

    website_subtitle = models.CharField(max_length = 100, null = False, blank = True, default = '',
            verbose_name = _(u'Subtítulo del sitio'),
            help_text = _(u'Un subtítulo opcional, que aparecerá debajo del nombre global'))

    website_description = models.TextField(null = False, blank = False,
            verbose_name = _(u'Descripción del sitio'),
            help_text = _(u'Texto plano que aparece en el head html de todas las páginas.'))

    footer_line = models.TextField(null = False, blank = False,
            verbose_name = _(u'Línea pie de página'),
            help_text = _(u'Texto HTML que aparece en la línea de pie de todas las páginas.'))

    # Maximum bounds of the map
    map_bounds_left = models.FloatField(null = False, blank = False, default = -20037508.34,
            verbose_name = _(u'Extensión izqda'),
            help_text = _(u'Extensión máxima del mapa (por defecto, el planeta entero).'))

    map_bounds_right = models.FloatField(null = False, blank = False, default = 20037508.34,
            verbose_name = _(u'Extensión derecha'),
            help_text = _(u'Extensión máxima del mapa (por defecto, el planeta entero).'))

    map_bounds_bottom = models.FloatField(null = False, blank = False, default = -20037508.34,
            verbose_name = _(u'Extensión inferior'),
            help_text = _(u'Extensión máxima del mapa (por defecto, el planeta entero).'))

    map_bounds_top = models.FloatField(null = False, blank = False, default = 20037508.34,
            verbose_name = _(u'Extensión superior'),
            help_text = _(u'Extensión máxima del mapa (por defecto, el planeta entero).'))

    # Map configuration
    map_zoom_levels = models.IntegerField(null = False, blank = False, default = 18,
            verbose_name = _(u'Niveles de zoom'),
            help_text = _(u'Número total de niveles del mapa.'))

    map_max_resolution = models.IntegerField(null = False, blank = False, default = 156543,
            verbose_name = _(u'Resolución máxima'),
            help_text = _(u'Resolución máxima del mapa.'))

    map_units = models.CharField(max_length = 50, null = False, blank = False, default = 'meters',
            verbose_name = _(u'Unidades del mapa'),
            help_text = _(u'Unidad usada en la extensión del mapa y otros sitios.'))

    # Map initial position
    map_initial_lon = models.FloatField(null = False, blank = False,
            verbose_name = _(u'Longitud inicial'),
            help_text = _(u'Posición inicial del mapa (longitud).'))

    map_initial_lat = models.FloatField(null = False, blank = False,
            verbose_name = _(u'Latitud inicial'),
            help_text = _(u'Posición inicial del mapa (latitud).'))

    map_initial_zoom = models.IntegerField(null = False, blank = False,
            verbose_name = _(u'Zoom inicial'),
            help_text = _(u'Posición inicial del mapa (zoom).'))

    # Entry proposal forms
    new_entity_proposal_enabled = models.BooleanField(null = False, blank = True, default = False,
            verbose_name = _(u'Activar formulario de nueva entidad.'),
            help_text = _(u'''
Si está activo, podrás añadir una opción de menú con url /entity_proposal/new/ para
ver el formulario de proponer nuevas entidades.
'''))

    entity_change_proposal_enabled = models.BooleanField(null = False, blank = True, default = False,
            verbose_name = _(u'Activar formulario de modificar entidad.'),
            help_text = _(u'''
Si está activo, la ficha de entidad tendrá un enlace que lleve al formulario de
proponer cambios.
'''))

    new_entity_proposal_title = models.CharField(max_length = 100, null = False, blank = True,
            verbose_name = _(u'Título del formulario (nueva entidad)'),
            help_text = _(u'Título alternativo para el formulario de solicitud de nueva entidad.'))

    new_entity_proposal_text = models.TextField(null = False, blank = True,
            verbose_name = _(u'Texto del formulario (nueva entidad)'),
            help_text = _(u'Texto alternativo para el formulario de solicitud de nueva entidad.'))

    change_proposal_title = models.CharField(max_length = 100, null = False, blank = True,
            verbose_name = _(u'Título del formulario (modificación)'),
            help_text = _(u'Título alternativo para el formulario de solicitud de modificación de entidad.'))

    change_proposal_text = models.TextField(null = False, blank = True,
            verbose_name = _(u'Texto del formulario (modificación)'),
            help_text = _(u'Texto alternativo para el formulario de solicitud de de modificación de entidad..'))

    proposal_bottom_text = models.TextField(null = False, blank = True,
            verbose_name = _(u'Texto inferior'),
            help_text = _(u'Texto alternativo que aparece en la parte inferior del formulario.'))

    # Form fields visibility control
    proponent_email_field_enabled = models.BooleanField(null = False, blank = True, default = True,
            verbose_name = _(u'Mail del proponente.'))
    proponent_comment_field_enabled = models.BooleanField(null = False, blank = True, default = True,
            verbose_name = _(u'Comentarios.'))
    alias_field_enabled = models.BooleanField(null = False, blank = True, default = True,
            verbose_name = _(u'Alias.'))
    summary_field_enabled = models.BooleanField(null = False, blank = True, default = True,
            verbose_name = _(u'Resumen.'))
    subcategories_field_enabled = models.BooleanField(null = False, blank = True, default = True,
            verbose_name = _(u'Categorías.'))
    address_1_field_enabled = models.BooleanField(null = False, blank = True, default = True,
            verbose_name = _(u'Dirección (calle y nº).'))
    address_2_field_enabled = models.BooleanField(null = False, blank = True, default = True,
            verbose_name = _(u'Dirección (resto).'))
    zipcode_field_enabled = models.BooleanField(null = False, blank = True, default = True,
            verbose_name = _(u'Codigo Postal.'))
    city_field_enabled = models.BooleanField(null = False, blank = True, default = True,
            verbose_name = _(u'Ciudad.'))
    province_field_enabled = models.BooleanField(null = False, blank = True, default = True,
            verbose_name = _(u'Provincia.'))
    country_field_enabled = models.BooleanField(null = False, blank = True, default = True,
            verbose_name = _(u'País.'))
    zone_field_enabled = models.BooleanField(null = False, blank = True, default = True,
            verbose_name = _(u'Zona.'))
    latitude_field_enabled = models.BooleanField(null = False, blank = True, default = True,
            verbose_name = _(u'Latitud.'))
    longitude_field_enabled = models.BooleanField(null = False, blank = True, default = True,
            verbose_name = _(u'Longitud.'))
    contact_phone_1_field_enabled = models.BooleanField(null = False, blank = True, default = True,
            verbose_name = _(u'Teléfono de contacto 1.'))
    contact_phone_2_field_enabled = models.BooleanField(null = False, blank = True, default = True,
            verbose_name = _(u'Teléfono de contacto 2.'))
    fax_field_enabled = models.BooleanField(null = False, blank = True, default = True,
            verbose_name = _(u'Fax.'))
    email_field_enabled = models.BooleanField(null = False, blank = True, default = True,
            verbose_name = _(u'Email 1.'))
    email_2_field_enabled = models.BooleanField(null = False, blank = True, default = True,
            verbose_name = _(u'Email 2.'))
    web_field_enabled = models.BooleanField(null = False, blank = True, default = True,
            verbose_name = _(u'Web 1.'))
    web_2_field_enabled = models.BooleanField(null = False, blank = True, default = True,
            verbose_name = _(u'Web 2.'))
    contact_person_field_enabled = models.BooleanField(null = False, blank = True, default = True,
            verbose_name = _(u'Persona de contacto.'))
    creation_year_field_enabled = models.BooleanField(null = False, blank = True, default = True,
            verbose_name = _(u'Año de creación.'))
    legal_form_field_enabled = models.BooleanField(null = False, blank = True, default = True,
            verbose_name = _(u'Forma jurídica.'))
    description_field_enabled = models.BooleanField(null = False, blank = True, default = True,
            verbose_name = _(u'Descripción.'))
    goals_field_enabled = models.BooleanField(null = False, blank = True, default = True,
            verbose_name = _(u'Objetivo como entidad.'))
    finances_field_enabled = models.BooleanField(null = False, blank = True, default = True,
            verbose_name = _(u'Finanzas.'))
    social_values_field_enabled = models.BooleanField(null = False, blank = True, default = True,
            verbose_name = _(u'Valores sociales y medioambientales.'))
    how_to_access_field_enabled = models.BooleanField(null = False, blank = True, default = True,
            verbose_name = _(u'Forma de acceso.'))
    networks_member_field_enabled = models.BooleanField(null = False, blank = True, default = True,
            verbose_name = _(u'Redes de las que forma parte.'))
    networks_works_with_field_enabled = models.BooleanField(null = False, blank = True, default = True,
            verbose_name = _(u'Otras entidades con las que colabora.'))
    ongoing_projects_field_enabled = models.BooleanField(null = False, blank = True, default = True,
            verbose_name = _(u'Proyectos en marcha.'))
    needs_field_enabled = models.BooleanField(null = False, blank = True, default = True,
            verbose_name = _(u'Necesidades.'))
    offerings_field_enabled = models.BooleanField(null = False, blank = True, default = True,
            verbose_name = _(u'Qué ofrece.'))
    additional_info_field_enabled = models.BooleanField(null = False, blank = True, default = True,
            verbose_name = _(u'Información adicional.'))

    # Hints
    description_hints = models.TextField(null = False, blank = True, default = '',
            verbose_name = _(u'Ayuda para Descripción'))
    goals_hints = models.TextField(null = False, blank = True, default = '',
            verbose_name = _(u'Ayuda para Objetivo como entidad'))
    finances_hints = models.TextField(null = False, blank = True, default = '',
            verbose_name = _(u'Ayuda para Finanzas'))
    social_values_hints = models.TextField(null = False, blank = True, default = '',
            verbose_name = _(u'Ayuda para Valores sociales y medioambientales'))
    how_to_access_hints = models.TextField(null = False, blank = True, default = '',
            verbose_name = _(u'Ayuda para Forma de acceso'))
    networks_member_hints = models.TextField(null = False, blank = True, default = '',
            verbose_name = _(u'Ayuda para Redes de las que forma parte'))
    networks_works_with_hints = models.TextField(null = False, blank = True, default = '',
            verbose_name = _(u'Ayuda para Otras entidades con las que colabora'))
    ongoing_projects_hints = models.TextField(null = False, blank = True, default = '',
            verbose_name = _(u'Ayuda para Proyectos en marcha'))
    needs_hints = models.TextField(null = False, blank = True, default = '',
            verbose_name = _(u'Ayuda para Necesidades'))
    offerings_hints = models.TextField(null = False, blank = True, default = '',
            verbose_name = _(u'Ayuda para Qué ofrece'))
    additional_info_hints = models.TextField(null = False, blank = True, default = '',
            verbose_name = _(u'Ayuda para Información adicional'))

    def __unicode__(self):
        return self.website_name

    def save(self, *args, **kwargs):
        super(self.__class__, self).save(*args, **kwargs)
        # When changing SiteInfo, force reloading the current Site
        Site.objects.clear_cache()

    class Meta:
	ordering = ['website_name']
	verbose_name = _(u'info sitio')
	verbose_name_plural = _(u'info sitios')


class EntityType(models.Model):
    '''
    The organization type of the entity, structurally speaking.
    '''
    name = models.CharField(max_length = 100, null = False, blank = False,
            verbose_name = _(u'Nombre'))

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = _(u'tipo de entidad')
        verbose_name_plural = _(u'tipos de entidad')


class CategoryActiveManager(models.Manager):
    '''With this manager you only see active categories.'''

    def actives_only(self):
        queryset = self.get_query_set()
        return queryset.filter(is_active=True)


class Category(models.Model):
    '''
    First classification level.
    '''
    name = models.CharField(max_length = 100, null = False, blank = False,
            verbose_name = _(u'Nombre'))
    slug = models.SlugField(max_length = 100, null = False, blank = False, unique = True,
            verbose_name = _(u'Slug'),
            help_text = _(u'Podrás consultar la categoría en la dirección /map/&lt;slug&gt;/'))
    description = models.TextField(null = False, blank = True,
            verbose_name = _(u'Descripción'))
    marker_url = models.CharField(max_length = 100, null = False, blank = True, default = '',
            verbose_name = _(u'Marcador'),
            help_text = _(u'''
Indicar la ruta de la imagen a usar como marcador. La imagen debe ser un fichero .jpg, .png o .gif de 32x37 pixels<br/>
con el punto de inserción en el centro del borde inferior.<br/>
La ruta será:<br/>
 - img/markers/icons/&lt;nombre_icono&gt;.png para los iconos predefinidos de Macadjan (clásicos)<br/>
 - img/markers/icons-noun-project/&lt;nombre_icono&gt;.png para los iconos nuevos<br/>
Si no se indica marcador, se usará el marcador por defecto definido en settings.py.<br/>
La lista de iconos disponibles es la siguiente:<br/>
 - https://n-1.cc/pg/file/read/1268597/iconos-disponibles-para-los-marcadores-de-macadjan<br/>
 - https://n-1.cc/file/view/1521147/iconos-disponibles-para-los-marcadores-de-macadjan-nuevos
'''))
    is_active = models.BooleanField(default = False,
            verbose_name = _(u'Activo'),
            help_text = _(u'Indica si esta categoría está activa; si no lo está, no saldrá en el árbol de clasificación del mapa.'))

    objects = CategoryActiveManager()

    def __unicode__(self):
        return self.name

    def to_dict(self, include_subcategories = False):
        the_dict = {
            "id": self.id,
            "name": self.name,
            "slug": self.slug,
            "description": self.description,
            "markerUrl": self.marker_url,
            "is_active": self.is_active,
        }
        if include_subcategories:
            the_dict['subcategories'] = [
                subcat.to_dict() for subcat in self.subcategories.filter(is_active = True)
            ]
        return the_dict

    @property
    def active_subcategories(self):
        return self.subcategories.filter(is_active = True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify_uniquely(self.name, self.__class__)
        super(self.__class__, self).save(*args, **kwargs)

    class Meta:
        ordering = ['name']
        verbose_name = _(u'categoría')
        verbose_name_plural = _(u'categorías')


class SubCategoryActiveManager(models.Manager):
    '''With this manager you only see active subcategories.'''

    def actives_only(self):
        queryset = self.get_query_set()
        return queryset.filter(is_active=True)


class SubCategory(models.Model):
    '''
    Second classification level. A subcategory is included inside a category.
    '''
    name = models.CharField(max_length = 100, null = False, blank = False,
            verbose_name = _(u'Nombre'))
    category = models.ForeignKey("macadjan.Category", related_name = 'subcategories', null = False, blank = False,
            on_delete = models.CASCADE,
            verbose_name = _(u'Categoría'))
    slug = models.SlugField(max_length = 100, null = False, blank = False, unique = True,
            verbose_name = _(u'Slug'),
            help_text = _(u'Podrás consultar la subcategoría en la dirección /map/&lt;slug_categoría&gt;/&lt;slug_subcategoría&gt;/'))
    description = models.TextField(null = False, blank = True,
            verbose_name = _(u'Descripción'))
    marker_url = models.CharField(max_length = 100, null = False, blank = True, default = '',
            verbose_name = _(u'Marcador'),
            help_text = _(u'''
Indicar la ruta de la imagen a usar como marcador. La imagen debe ser un fichero .jpg, .png o .gif de 32x37 pixels<br/>
con el punto de inserción en el centro del borde inferior.<br/>
La ruta será:<br/>
 - img/markers/icons/&lt;nombre_icono&gt;.png para los iconos predefinidos de Macadjan (clásicos)<br/>
 - img/markers/icons-noun-project/&lt;nombre_icono&gt;.png para los iconos nuevos<br/>
Si no se indica marcador, se usará el marcador de la categoría a la que pertenece esta subcategoría.<br/>
La lista de iconos disponibles es la siguiente:<br/>
 - https://n-1.cc/pg/file/read/1268597/iconos-disponibles-para-los-marcadores-de-macadjan<br/>
 - https://n-1.cc/file/view/1521147/iconos-disponibles-para-los-marcadores-de-macadjan-nuevos
'''))
    is_active = models.BooleanField(default = False,
            verbose_name = _(u'Activo'),
            help_text = _(u'Indica si esta subcategoría está activa; si no lo está, no saldrá en el árbol de clasificación del mapa.'))

    objects = SubCategoryActiveManager()

    def __unicode__(self):
        return u'%s - %s' % (self.category.name, self.name)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify_uniquely(self.name, self.__class__)
        super(self.__class__, self).save(*args, **kwargs)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "category_id": self.category.id,
            "slug": self.slug,
            "description": self.description,
            "markerUrl": self.marker_url,
            "is_active": self.is_active,
        }

    class Meta:
        ordering = ['category', 'name']
        verbose_name = _(u'subcategoría')
        verbose_name_plural = _(u'subcategorías')


class TagCollection(models.Model):
    '''
    A group of semantically related tags.
    '''
    name = models.CharField(max_length = 100, null = False, blank = False,
            verbose_name = _(u'Nombre'))
    slug = models.SlugField(max_length = 100, null = False, blank = False, unique = True,
            verbose_name = _(u'Slug'))

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify_uniquely(self.name, self.__class__)
        super(self.__class__, self).save(*args, **kwargs)

    class Meta:
        ordering = ['name']
        verbose_name = _(u'colección de etiquetas')
        verbose_name_plural = _(u'colecciones de etiquetas')


class EntityTag(models.Model):
    '''
    Arbitrary string that can be attachedd to entities.
    '''
    name = models.CharField(max_length = 100, null = False, blank = False,
            verbose_name = _(u'Nombre'))
    slug = models.SlugField(max_length = 100, null = False, blank = False, unique = True,
            verbose_name = _(u'Slug'))
    collection = models.ForeignKey("macadjan.TagCollection", related_name = 'tags', null = False, blank = False,
            on_delete = models.CASCADE,
            verbose_name = _(u'Colección'))

    def __unicode__(self):
        return u'%s - %s' % (self.collection.name, self.name)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify_uniquely(self.name, self.__class__)
        super(self.__class__, self).save(*args, **kwargs)

    class Meta:
        ordering = ['collection', 'name']
        verbose_name = _(u'etiqueta')
        verbose_name_plural = _(u'etiquetas')


class MapSource(models.Model):
    '''
    A people group in charge of collecting and processing entities.
    '''
    name = models.CharField(max_length = 100, null = False, blank = False,
            verbose_name = _(u'Nombre'))
    slug = models.SlugField(max_length = 100, null = False, blank = True, unique = True,
            verbose_name = _(u'Slug'),
            help_text = _(u'Podrás consultar la fuente en la dirección /map-source/&lt;slug&gt;/'))
    description = models.TextField(null = False, blank = True,
            verbose_name = _(u'Descripción'))
    web = models.URLField(null = False, blank = True, default = '',
            verbose_name = _(u'Web'),
            help_text = _(u'Página web informativa. Ojo: hay que poner la dirección completa, incluyendo http://. La dirección será validada automáticamente para comprobar que existe.'))

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify_uniquely(self.name, self.__class__)
        super(self.__class__, self).save(*args, **kwargs)

    class Meta:
        ordering = ['name']
        verbose_name = _(u'fuente de mapeo')
        verbose_name_plural = _(u'fuentes de mapeo')


class MacadjanUserProfile(models.Model):
    '''
    A User profile that may link one user with a MapSource, in order to automatically
    set the map source when creating objects, and to limit her to only access objects
    of this source. This only makes sense for "staff" users (admins still will have
    access to any object, and non-staff will not be able to use the admin).
    '''
    user = models.OneToOneField('auth.User', related_name = 'macadjan_profile', null = False, blank = False,
            on_delete = models.CASCADE,
            verbose_name = _(u'Usuario'))
    map_source = models.ForeignKey("macadjan.MapSource", related_name = 'user_profiles', null = True, blank = True,
            on_delete = models.SET_NULL,
            verbose_name = _(u'Fuente de mapeo'),
            help_text = _(u'Sólo tiene sentido para usuarios staff (no admin). Si ponemos una fuente, '
                          u'este usuario sólo podrá trabajar con entidades de esta fuente.'))

    class Meta:
        ordering = ['user']
        verbose_name = _(u'perfil Macadjan')
        verbose_name_plural = _(u'perfiles Macadjan')


class EntityManager(models.Manager):

    def entities_in_area(self, left, right, top, bottom):
        '''
        Search all entities located inside a geographical area.
        '''
        return self.get_query_set().filter(
                            longitude__gte = left, longitude__lt = right,
                            latitude__gte = bottom, latitude__lt = top)

    def entities_without_area(self):
        '''
        Search all entities without geographical area.
        '''
        return self.get_query_set().filter(
                            longitude__isnull = True, latitude__isnull = True)

    def entities_with_area(self):
        '''
        Search all entities with geographical area.
        '''
        return self.get_query_set().filter(
                            longitude__isnull = False, latitude__isnull = False)

    def filter_by_cat(self, entities, category = None, subcategory = None):
        '''
        Add a filter by category or subcategory.
        '''
        if subcategory:
            entities = entities.filter(subcategories = subcategory)
        elif category:
            entities = entities.filter(subcategories__category = category).distinct()
        return entities

    def filter_with_source(self, entities, map_source):
        '''
        Add a further filter with map source.
        '''
        if map_source:
            entities = entities.filter(map_source = map_source)
        return entities

    def filter_with_keywords(self, entities, keywords):
        '''
        Add a further filter with keywords.
        '''
        if not keywords or not entities:
            return entities
        entity_ids = SearchQuerySet().filter(content=keywords).values_list('pk', flat=True)
        entities = entities.filter(pk__in = entity_ids)
        return entities


class EntityActiveManager(EntityManager):
    '''With this manager you only see active entities.'''
    def get_query_set(self):
        return super(EntityActiveManager, self).get_query_set().filter(is_active = True)


class Entity(models.Model):
    '''
    Main class of MaCaDjan project: it represents a mapped entity.

    On save, a slug is automatically generated if not set. Also the creation_date and modification_date
    are automatically set, unless you provide the "update_dates = False" argument to save().
    '''

    # General info
    name = models.CharField(max_length = 100, null = False, blank = False,
            verbose_name = _(u'Nombre'),
            help_text = _(u'Nombre de la entidad (para salir en el globo).'))
    slug = models.SlugField(max_length = 100, null = False, blank = False, unique = True,
            verbose_name = _(u'Slug'),
            help_text = _(u'Identificador de la entidad, sólo puede contener letras, números y el signo "_". Si lo dejas en blanco se generará automáticamente.<br/>Podrás consultar la entidad en la dirección /entity/&lt;slug&gt;/'))
    alias = models.CharField(max_length = 100, null = False, blank = True, default = '',
            verbose_name = _(u'Alias'),
            help_text = _(u'Un posible nombre alternativo para la entidad.'))
    summary = models.CharField(max_length = 300, null = False, blank = True,
            verbose_name = _(u'Resumen'),
            help_text = _(u'Define la entidad en una frase.'))

    # Container info
    is_container = models.BooleanField(
            verbose_name = _(u'Es contenedor'),
            help_text = _(u'Indica si esta entidad puede contener otras, las cuales comparten espacio físico con ellas (ej. un CSOA, una cooperativa integral...).'))
    contained_in = models.ForeignKey('self', null = True, blank = True,
            on_delete = models.SET_NULL,
            limit_choices_to = {'is_container': True},
            verbose_name = _(u'Agrupada dentro de'),
            help_text = _(u'Indica si esta entidad está contenida en otra (ej. un taller dentro de un CSOA).'))

    # Geographical info
    latitude = models.FloatField(max_length = 100, null = True, blank = True,
            verbose_name = _(u'Latitud'),
            help_text = _(u'Usa la herramienta de la derecha para obtener la latitud.'))
    longitude = models.FloatField(max_length = 100, null = True, blank = True,
            verbose_name = _(u'Longitud'),
            help_text = _(u'Usa la herramienta de la derecha para obtener la longitud.'))
    address_1 = models.CharField(max_length = 100, null = False, blank = True, default = '',
            verbose_name = _(u'Dirección (calle y nº)'),
            help_text = _(u'Tipo y nombre de vía y número. Ejemplos: C/ del Pez, 21; Av. de la ilustración, 145'))
    address_2 = models.CharField(max_length = 100, null = False, blank = True, default = '',
            verbose_name = _(u'Dirección (resto)'),
            help_text = _(u'Portal, piso y otros datos. Ejemplos: Escalera A, 3º izq.; Local 4 entrada posterior.'))
    zipcode = models.CharField(max_length = 5, null = False, blank = True, default = '',
            verbose_name = _(u'Cód. postal'),
            help_text = _(u'Cinco dígitos. Ej. 28038'))
    city = models.CharField(max_length = 100, null = False, blank = True, default = '',
            verbose_name = _(u'Población'),
            help_text = _(u'Nombre de la población tal como se usa en la dirección postal. Ej. Madrid, Alcorcón.'))
    province = models.CharField(max_length = 100, null = False, blank = True, default = '',
            verbose_name = _(u'Provincia'),
            help_text = _(u'Nombre de la provincia, no es necesario si se llama igual que la ciudad.'))
    country = models.CharField(max_length = 100, null = False, blank = True, default = '',
            verbose_name = _(u'País'),
            help_text = _(u'Nombre del país, tal como se usa en la dirección postal, si es necesario.'))
    zone = models.CharField(max_length = 100, null = False, blank = True, default = '',
            verbose_name = _(u'Zona'),
            help_text = _(u'Zona de influencia de la entidad. Puede ser barrio, pueblo, ciudad, comarca, pedanía... Ej. Barrio de Lavapiés, Sierra Norte de Madrid.'))

    # Contact info
    contact_phone_1 = models.CharField(max_length = 100, null = False, blank = True, default = '',
            verbose_name = _(u'Teléfono contacto 1'),
            help_text = _(u'Un número de teléfono a quien llamar.'))
    contact_phone_2 = models.CharField(max_length = 100, null = False, blank = True, default = '',
            verbose_name = _(u'Teléfono contacto 2'),
            help_text = _(u'Se pueden poner dos teléfonos, ejemplo un fijo y un móvil.'))
    fax = models.CharField(max_length = 100, null = False, blank = True, default = '',
            verbose_name = _(u'Fax'),
            help_text = _(u'También se puede poner un número de fax.'))
    email = models.EmailField(null = False, blank = True, default = '',
            verbose_name = _(u'Email 1'),
            help_text = _(u'Email de contacto. Ojo: poner la dirección correcta y sin añadir espacios a izquierda ni derecha. Ej. colectivo@gmail.com'))
    email_2 = models.EmailField(null = False, blank = True, default = '',
            verbose_name = _(u'Email 2'),
            help_text = _(u'Se puede poner un segundo email de contacto.'))
    web = models.URLField(null = False, blank = True, default = '',
            verbose_name = _(u'Web 1'),
            help_text = _(u'Página web informativa. Ojo: hay que poner la dirección completa, incluyendo http://. La dirección será validada automáticamente para comprobar que existe.'))
    web_2 = models.URLField(null = False, blank = True, default = '',
            verbose_name = _(u'Web 2'),
            help_text = _(u'Se puede poner una segunda página web.'))
    contact_person = models.CharField(max_length = 100, null = False, blank = True, default = '',
            verbose_name = _(u'Persona contacto'),
            help_text = _(u'Nombre de al menos una persona por quien preguntar.'))

    # Accounting info (source may be NULL in internal operations, but you must fill it in the forms; dates are updated automatically on save)
    creation_date = models.DateTimeField(null = False, blank = True,
            verbose_name = _(u'Fecha de alta'),
            help_text = _(u'Fecha y hora de alta de esta entidad en la base de datos.'))
    modification_date = models.DateTimeField(null = False, blank = True,
            verbose_name = _(u'Fecha de última modificación'),
            help_text = _(u'Fecha y hora de última modificación de esta entidad.'))

    # Entity active/inactive
    is_active = models.BooleanField(default = False,
            verbose_name = _(u'Activa'),
            help_text = _(u'Indica si esta entidad está activa; si no lo está, no saldrá en el mapa ni en los listados.'))

    # Entity type (may be NULL in internal operations, but you must fill it in the forms)
    entity_type = models.ForeignKey("macadjan.EntityType", related_name = 'entities', null = True, blank = False,
            on_delete = models.PROTECT,
            verbose_name = _(u'Tipo de entidad'),
            help_text = _(u'De qué tipo organizativo es la entidad, estructuralmente hablando.'))

    # Categories are associated transitively, through subcategories. If an entity does not have any specific
    # subcategory, link it to 'Others'. The main one may be NULL in internal operations, but you must fill it in the forms
    main_subcategory = models.ForeignKey("macadjan.SubCategory", related_name='entities_main', null=True, blank=False,
            on_delete = models.PROTECT,
            limit_choices_to = {'is_active': True},
            verbose_name = _(u'Categoría principal'),
            help_text = _(u'Determinará el tipo de icono en el mapa. Esta categoría deberá estar incluida en la lista de más abajo; si no, será añadida automáticamente.'))

    subcategories = models.ManyToManyField(SubCategory, related_name = 'entities', blank = True,
            limit_choices_to = {'is_active': True},
            verbose_name = _(u'Categorías'))

    # One entity can have as many tags as it wants.
    tags = models.ManyToManyField('macadjan.EntityTag', related_name = 'entities', blank = True,
            verbose_name = _(u'Etiquetas'))

    # Map source
    map_source = models.ForeignKey('macadjan.MapSource', related_name = 'entities', null = True, blank = False,
            on_delete = models.PROTECT,
            verbose_name = _(u'Fuente'),
            help_text = _('Colectivo encargado de crear y mantener los datos de esta entidad.'))

    # Define two custom object managers
    objects = EntityManager()
    objects_active = EntityActiveManager()

    def __unicode__(self):
        return self.name

    def save(self, update_dates = True, *args, **kwargs):
        if not self.slug:
            self.slug = slugify_uniquely(self.name, self.__class__)
        datetime_now = datetime.now()
        if update_dates:
            if not self.id:
                self.creation_date = datetime_now
            self.modification_date = datetime_now
        else:
            if self.creation_date == None:         # In any case there must be any dates
                self.creation_date = datetime_now
            if self.modification_date == None:
                self.modification_date = datetime_now
        super(Entity, self).save(*args, **kwargs)
        if self.main_subcategory and not (self.main_subcategory in self.subcategories.all()):
            self.subcategories.add(self.main_subcategory)

    @property
    def categories(self):
        return Category.objects.filter(id__in = self.subcategories.values_list('category_id'))

    @property
    def active_categories(self):
        return self.categories.filter(is_active = True)

    @property
    def active_subcategories(self):
        return self.subcategories.filter(is_active = True)

    @models.permalink
    def get_absolute_url(self):
        return ('entity', (), {'entity_slug': self.slug})

    @property
    def marker_url(self):
        marker_url = ''
        main_subcategory = self.main_subcategory
        if main_subcategory:
            marker_url = main_subcategory.marker_url
            if not marker_url:
                marker_url = main_subcategory.category.marker_url
        if not marker_url:
            marker_url = getattr(settings, 'DEFAULT_MARKER_URL', '')
        if not marker_url:
            raise ValueError(_(u'Debes definir el DEFAULT_MARKER_URL en los settings.'))
        return marker_url

    class Meta:
        abstract = True
        ordering = ['name']
        verbose_name = _(u'entidad')
        verbose_name_plural = _(u'entidades')


## NOTE: don't know very well why this method is necessary, and it's not enough with the save method.
## I don't also know what exactly happens with the fact that when we call add in this method, the
## signal fires again. But this seems to work.
#def entity_m2m_changed_event(sender, instance, action, reverse, model, pk_set, **kwargs):
#    if action == 'post_add' or action == 'post_remove' or action == 'post_clear':
#        if not (instance.main_subcategory in instance.subcategories.all()):
#            instance.subcategories.add(instance.main_subcategory)
#
#signals.m2m_changed.connect(entity_m2m_changed_event, sender=Entity.subcategories.through)

