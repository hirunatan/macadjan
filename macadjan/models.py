# -*- coding: utf-8 -*-

from datetime import datetime
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.sites.models import Site
from django.db.models import signals
from django.conf import settings
from django.core.mail import EmailMessage
from django.template import RequestContext, Context, loader
from haystack import query
from utils import slugify_uniquely
from macadjan_base.async_tasks import task__geolocalize_entity

class EntityType(models.Model):
    '''
    The organization type of the entity, structurally speaking.
    '''
    name = models.CharField(max_length = 100, null = False, blank = False,
            verbose_name = _(u'Nombre'))

    def __unicode__(self):
        return self.name

    class Meta:
        app_label = 'macadjan_base'
	ordering = ['name']
	verbose_name = _(u'tipo de entidad')
	verbose_name_plural = _(u'tipos de entidad')


class CategoryActiveManager(models.Manager):
    '''With this manager you only see active categories.'''
    def get_query_set(self):
        return super(CategoryActiveManager, self).get_query_set().filter(is_active = True)


class Category(models.Model):
    '''
    First classification level.
    '''
    name = models.CharField(max_length = 100, null = False, blank = False,
            verbose_name = _(u'Nombre'))
    slug = models.SlugField(max_length = 100, null = False, blank = True, unique = True,
            verbose_name = _(u'Slug'))
    description = models.TextField(null = False, blank = True,
            verbose_name = _(u'Descripción'))
    marker_url = models.CharField(max_length = 100, null = False, blank = True, default = '',
            verbose_name = _(u'Marcador'),
            help_text = _(u'''
Indicar la ruta de la imagen a usar como marcador. La imagen debe ser un fichero .jpg, .png o .gif de 32x37 pixels<br/>
con el punto de inserción en el centro del borde inferior.<br/>
La ruta será macadjan_base/markers/icons/&lt;nombre_icono&gt;.png para los iconos predefinidos de Macadjan, o bien<br/>
themes/&lt;nombre_tema&gt;/markers/&lt;nombre_icono&gt;.png para los iconos personalizados de un tema.<br/>
Si no se indica marcador, se usará el marcador por defecto definido en settings.py.
'''))
    is_active = models.BooleanField(default = False,
            verbose_name = _(u'Activo'),
            help_text = _(u'Indica si esta categoría está activa; si no lo está, no saldrá en el árbol de clasificación del mapa.'))

    # Define one normal object manager and one custom
    objects = models.Manager()
    objects_active = CategoryActiveManager()

    def __unicode__(self):
        return self.name

    @property
    def active_subcategories(self):
        return self.subcategories.filter(is_active = True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify_uniquely(self.name, self.__class__)
        super(self.__class__, self).save(*args, **kwargs)

    class Meta:
        app_label = 'macadjan_base'
	ordering = ['name']
	verbose_name = _(u'categoría')
	verbose_name_plural = _(u'categorías')


class SubCategory(models.Model):
    '''
    Second classification level. A subcategory is included inside a category.
    '''
    name = models.CharField(max_length = 100, null = False, blank = False,
            verbose_name = _(u'Nombre'))
    category = models.ForeignKey(Category, related_name = 'subcategories', null = False, blank = False,
            on_delete = models.CASCADE,
            verbose_name = _(u'Categoría'))
    slug = models.SlugField(max_length = 100, null = False, blank = True, unique = True,
            verbose_name = _(u'Slug'))
    description = models.TextField(null = False, blank = True,
            verbose_name = _(u'Descripción'))
    marker_url = models.CharField(max_length = 100, null = False, blank = True, default = '',
            verbose_name = _(u'Marcador'),
            help_text = _(u'''
Indicar la ruta de la imagen a usar como marcador. La imagen debe ser un fichero .jpg, .png o .gif de 32x37 pixels<br/>
con el punto de inserción en el centro del borde inferior.<br/>
La ruta será macadjan_base/markers/icons/&lt;nombre_icono&gt;.png para los iconos predefinidos de Macadjan, o bien<br/>
themes/&lt;nombre_tema&gt;/markers/&lt;nombre_icono&gt;.png para los iconos personalizados de un tema.<br/>
Si no se indica marcador, se usará el marcador de la categoría a la que pertenece esta subcategoría.
'''))
    is_active = models.BooleanField(default = False,
            verbose_name = _(u'Activo'),
            help_text = _(u'Indica si esta subcategoría está activa; si no lo está, no saldrá en el árbol de clasificación del mapa.'))

    def __unicode__(self):
        return u'%s - %s' % (self.category.name, self.name)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify_uniquely(self.name, self.__class__)
        super(self.__class__, self).save(*args, **kwargs)

    class Meta:
        app_label = 'macadjan_base'
	ordering = ['category', 'name']
	verbose_name = _(u'subcategoría')
	verbose_name_plural = _(u'subcategorías')


class TagCollection(models.Model):
    '''
    A group of semantically related tags.
    '''
    name = models.CharField(max_length = 100, null = False, blank = False,
            verbose_name = _(u'Nombre'))
    slug = models.SlugField(max_length = 100, null = False, blank = True, unique = True,
            verbose_name = _(u'Slug'))

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify_uniquely(self.name, self.__class__)
        super(self.__class__, self).save(*args, **kwargs)

    class Meta:
        app_label = 'macadjan_base'
	ordering = ['name']
	verbose_name = _(u'colección de etiquetas')
	verbose_name_plural = _(u'colecciones de etiquetas')


class EntityTag(models.Model):
    '''
    Arbitrary string that can be attachedd to entities.
    '''
    name = models.CharField(max_length = 100, null = False, blank = False,
            verbose_name = _(u'Nombre'))
    slug = models.SlugField(max_length = 100, null = False, blank = True, unique = True,
            verbose_name = _(u'Slug'))
    collection = models.ForeignKey(TagCollection, related_name = 'tags', null = False, blank = False,
            on_delete = models.CASCADE,
            verbose_name = _(u'Colección'))

    def __unicode__(self):
        return u'%s - %s' % (self.collection.name, self.name)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify_uniquely(self.name, self.__class__)
        super(self.__class__, self).save(*args, **kwargs)

    class Meta:
        app_label = 'macadjan_base'
	ordering = ['collection', 'name']
	verbose_name = _(u'etiqueta')
	verbose_name_plural = _(u'etiquetas')


class EntityManager(models.Manager):

    def entities_in_area(self, left, right, top, bottom, category = None, subcategory = None, map_source = None):
        '''
        Search all entities located inside a geographical area, optionally filtering
        by category or subcategory and map_source.
        '''
        entities = super(EntityManager, self).get_query_set().filter(
                            longitude__gte = left, longitude__lt = right,
                            latitude__gte = bottom, latitude__lt = top)
        return self._entities_filter(entities, category, subcategory, map_source)

    def entities_without_area(self, category = None, subcategory = None, map_source = None):
        '''
        Search all entities without geographical area, optionally filtering by category
        or subcategory and map_source.
        '''
        entities = super(EntityManager, self).get_query_set().filter(
                            longitude__isnull = True, latitude__isnull = True)
        return self._entities_filter(entities, category, subcategory, map_source)

    def entities_with_area(self, category = None, subcategory = None, map_source = None):
        '''
        Search all entities with geographical area, optionally filtering by category
        or subcategory and map_source.
        '''
        entities = super(EntityManager, self).get_query_set().filter(
                            longitude__isnull = False, latitude__isnull = False)
        return self._entities_filter(entities, category, subcategory, map_source)

    def _entities_filter(self, base_queryset, category, subcategory, map_source):
        entities = base_queryset
        if subcategory:
            entities = entities.filter(subcategories = subcategory)
        elif category:
            entities = entities.filter(subcategories__category = category).distinct()
        if map_source:
            entities = entities.filter(map_source = map_source)
        return entities

    def filter_with_keywords(self, entities, keywords):
        '''
        Add a further filter with keywords. Warning: the returned object is no longer
        a QuerySet, but a list.
        '''
        if not keywords:
            return list(entities)
        entities_text = query.RelatedSearchQuerySet().filter(content=keywords).load_all()
        entities_text = entities_text.load_all_queryset(Entity, entities)
        return [result.object for result in entities_text]


class EntityActiveManager(EntityManager):
    '''With this manager you only see active entities.'''
    def get_query_set(self):
        return super(EntityActiveManager, self).get_query_set().filter(is_active = True)

    def entities_in_area(self, left, right, top, bottom, category = None, subcategory = None, map_source = None):
        return super(EntityActiveManager, self).entities_in_area(left, right, top, bottom, category, subcategory, map_source).filter(is_active = True)

    def entities_without_area(self, category = None, subcategory = None, map_source = None):
        return super(EntityActiveManager, self).entities_without_area(category, subcategory, map_source).filter(is_active = True)

    def entities_with_area(self, category = None, subcategory = None, map_source = None):
        return super(EntityActiveManager, self).entities_with_area(category, subcategory, map_source).filter(is_active = True)


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
    slug = models.SlugField(max_length = 100, null = False, blank = True, unique = True,
            verbose_name = _(u'Slug'),
            help_text = _(u'Identificador de la entidad, sólo puede contener letras, números y el signo "_". Si lo dejas en blanco se generará automáticamente.'))
    alias = models.CharField(max_length = 100, null = False, blank = True, default = '',
            verbose_name = _(u'Alias'),
            help_text = _(u'Un posible nombre alternativo para la entidad.'))
    summary = models.CharField(max_length = 300, null = False, blank = True,
            verbose_name = _(u'Resumen'),
            help_text = _(u'Descripción breve (para salir en el globo).'))

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

    # Detailed descriptive info
    creation_year = models.IntegerField(null = True, blank = True,
            verbose_name = _(u'Año creación'),
            help_text = _(u'Año en que el colectivo u organización comenzó su actividad (introducir un nº con las cuatro cifras).'))
    legal_form = models.CharField(max_length = 100, null = False, blank = True, default = '',
            verbose_name = _(u'Forma jurídica'),
            help_text = _(u'Con qué forma jurídica concreta está registrada la entidad, si lo está.'))
    description = models.TextField(null = False, blank = True, default = '',
            verbose_name = _(u'Descripción'),
            help_text = _(u'Aquí se puede poner una descripción general, o cualquier cosa que no entre en las casillas siguientes. Si hay poca información, puede ser suficiente con rellenar esta casilla. Alternativamente, puede no ser necesaria si se han rellenado las otras con mucha información.'))
    goals = models.TextField(null = False, blank = True, default = '',
            verbose_name = _(u'Objetivo como entidad'),
            help_text = _(u'Objetivos principales de la entidad, cuál es su razón de ser; qué ofrece a sus socios, usuarios, clientes o público en general.'))
    finances = models.TextField(null = False, blank = True, default = '',
            verbose_name = _(u'Finanzas'),
            help_text = _(u'Indicar cómo gestiona el dinero (con/sin ánimo de lucro, precios de los productos si vende algo, fuentes de ingresos, modo de financiación...).'))
    social_values = models.TextField(null = False, blank = True, default = '',
            verbose_name = _(u'Valores sociales y medioambientales'),
            help_text = _(u'Justificación de por qué merece estar en este directorio, valores que aporta en función de nuestros criterios de selección, en tanto que relaciones humanas y cuidado del medio ambiente.'))
    how_to_access = models.TextField(null = False, blank = True, default = '',
            verbose_name = _(u'Forma de acceso'),
            help_text = _(u'Cómo acceder a los servicios o funciones de la entidad, horarios y lugar de contacto, condiciones de participación, venta o ditribución.'))
    networks_member = models.TextField(null = False, blank = True, default = '',
            verbose_name = _(u'Redes de las que forma parte'),
            help_text = _(u'Indicar si esta entidad está integrada en algún tipo de redes, grupo o plataforma, junto con otras entidades.'))
    networks_works_with = models.TextField(null = False, blank = True, default = '',
            verbose_name = _(u'Otras entidades con las que colabora'),
            help_text = _(u'Indicar si esta entidad trabaja en colaboración con otras entidades o redes, aún sin formar parte de ellas.'))
    ongoing_projects = models.TextField(null = False, blank = True, default = '',
            verbose_name = _(u'Proyectos en marcha'),
            help_text = _(u'Indicar, si se desea, los proyectos importantes que la entidad lleva a cabo o en los que está involucrada.'))
    needs = models.TextField(null = False, blank = True, default = '',
            verbose_name = _(u'Necesidades'),
            help_text = _(u'Indicar si la entidad tiene actualmente alguna necesidad importante que pudiera ser cubierta por otras entidades o personas externas.'))
    offerings = models.TextField(null = False, blank = True, default = '',
            verbose_name = _(u'Qué ofrece'),
            help_text = _(u'Indicar si esta entidad está en disposición de ofrecer recursos u otros elementos que puedan ser útiles a otras entidades relacionadas o personas externas; posibilidades de colaboración.'))
    additional_info = models.TextField(null = False, blank = True, default = '',
            verbose_name = _(u'Información adicional'),
            help_text = _(u'Cualquier otra información no clasificable en las casillas anteriores.'))

    # Accounting info (source may be NULL in internal operations, but you must fill it in the forms; dates are updated automatically on save)
    map_source = models.ForeignKey(MapSource, related_name = 'entities', null = True, blank = False,
            on_delete = models.PROTECT,
            verbose_name = _(u'Fuente'),
            help_text = _('Colectivo encargado de crear y mantener los datos de esta entidad.'))
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
    entity_type = models.ForeignKey(EntityType, related_name = 'entities', null = True, blank = False,
            on_delete = models.PROTECT,
            verbose_name = _(u'Tipo de entidad'),
            help_text = _(u'De qué tipo organizativo es la entidad, estructuralmente hablando.'))

    # Categories are associated transitively, through subcategories. If an entity does not have any specific
    # subcategory, link it to 'Others'. The main one may be NULL in internal operations, but you must fill it in the forms
    main_subcategory = models.ForeignKey(SubCategory, related_name = 'entities_main', null = True, blank = False,
            on_delete = models.PROTECT,
            limit_choices_to = {'is_active': True},
            verbose_name = _(u'Categoría principal'),
            help_text = _(u'Determinará el tipo de icono en el mapa. Esta categoría deberá estar incluida en la lista de más abajo; si no, será añadida automáticamente.'))

    subcategories = models.ManyToManyField(SubCategory, related_name = 'entities', blank = True,
            limit_choices_to = {'is_active': True},
            verbose_name = _(u'Categorías'))

    # One entity can have as many tags as it wants.
    tags = models.ManyToManyField('macadjan_base.EntityTag', related_name = 'entities', blank = True,
            verbose_name = _(u'Etiquetas'))

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
        super(self.__class__, self).save(*args, **kwargs)
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
        return ('base:entity', (), {'id_entity': self.id})

    class Meta:
        app_label = 'macadjan_base'
	ordering = ['name']
	verbose_name = _(u'entidad')
	verbose_name_plural = _(u'entidades')


# NOTE: don't know very well why this method is necessary, and it's not enough with the save method.
# I don't also know what exactly happens with the fact that when we call add in this method, the
# signal fires again. But this seems to work.
def entity_m2m_changed_event(sender, instance, action, reverse, model, pk_set, **kwargs):
    if action == 'post_add' or action == 'post_remove' or action == 'post_clear':
        if not (instance.main_subcategory in instance.subcategories.all()):
            instance.subcategories.add(instance.main_subcategory)

signals.m2m_changed.connect(entity_m2m_changed_event, sender=Entity.subcategories.through)


class EntityProposal(models.Model):
    '''
    A proposal that a external user has made for an entity, via the proposal form. It may be for a new
    entity or to modify data of an existing one.
    '''
    STATUS_PENDING = 'pending'
    STATUS_ACCEPTED = 'accepted'
    STATUS_REJECTED = 'rejected'
    STATUS_CHOICES = ((STATUS_PENDING, _(u'Pendiente')),
                      (STATUS_ACCEPTED, _(u'Aceptada')),
                      (STATUS_REJECTED, _(u'Rechazada')))

    # Main info
    existing_entity = models.ForeignKey(Entity, related_name = 'change_proposals', null = True, blank = True,
            on_delete = models.SET_NULL,
            verbose_name = _(u'Entidad existente'),
            help_text = _('Indica si esta propuesta es para cambiar los datos de una entidad existente (nulo si es para crear una entidad nueva).'))
    name = models.CharField(max_length = 100, null = False, blank = False,
            verbose_name = _(u'Nombre'),
            help_text = _(u'Nombre de la entidad (para salir en el globo).'))

    # Entity type
    entity_type = models.ForeignKey(EntityType, related_name = 'entity_proposals', null = False, blank = False,
            on_delete = models.PROTECT,
            verbose_name = _(u'Tipo de entidad'),
            help_text = _(u'De qué tipo organizativo es la entidad, estructuralmente hablando.'))

    # Main subcategory
    main_subcategory = models.ForeignKey(SubCategory, related_name = 'entity_proposals_main', null = False, blank = False,
            on_delete = models.PROTECT,
            limit_choices_to = {'is_active': True},
            verbose_name = _(u'Categoría principal'),
            help_text = _(u'Determinará el tipo de icono en el mapa.'))

    # Proponent info
    proponent_email = models.EmailField(null = False, blank = True, default = '',
            verbose_name = _(u'Email de quien hace la propuesta'),
            help_text = _(u'Si nos indicas tu email, te notificaremos cuando la procesemos y te podremos contactar para resolver dudas.'))
    proponent_comment = models.TextField(null = False, blank = True, default = '',
            verbose_name = _(u'Comentarios de la propuesta'),
            help_text = _(u'Cualquier cosa que nos quieras comentar acerca de la propuesta.'))

    # Accounting info
    status = models.CharField(max_length = 50, null = False, blank = False,
            default = STATUS_CHOICES[0][0],
            choices = STATUS_CHOICES,
            verbose_name = _(u'Estado de la propuesta'))
    status_info = models.TextField(null = False, blank = True, default = '',
            verbose_name = _(u'Respuesta a la propuesta (OJO, SE LE ENVIARÁ POR EMAIL AL PROPONENTE)'),
            help_text = _(u'Comentarios sobre la propuesta o información de por qué se ha aceptado o rechazado.'))
    internal_comment = models.TextField(null = False, blank = True, default = '',
            verbose_name = _(u'Comentarios internos (ESTO NO SALDRÁ DE AQUÍ)'),
            help_text = _(u'Notas internas de los administradores sobre la propuesta.'))
    map_source = models.ForeignKey(MapSource, related_name = 'entity_proposals', null = True, blank = False,
            on_delete = models.PROTECT,
            verbose_name = _(u'Fuente'),
            help_text = _('Colectivo encargado de crear y mantener los datos de esta entidad.'))
    creation_date = models.DateTimeField(null = False, blank = True,
            verbose_name = _(u'Fecha de alta'),
            help_text = _(u'Fecha y hora de envío de esta propuesta.'))
    modification_date = models.DateTimeField(null = False, blank = True,
            verbose_name = _(u'Fecha de última modificación'),
            help_text = _(u'Fecha y hora de última modificación de esta propuesta.'))

    # General description
    alias = models.CharField(max_length = 100, null = False, blank = True, default = '',
            verbose_name = _(u'Alias'),
            help_text = _(u'Un posible nombre alternativo para la entidad.'))
    summary = models.CharField(max_length = 300, null = False, blank = True,
            verbose_name = _(u'Resumen'),
            help_text = _(u'Descripción breve (para salir en el globo).'))

    # Other subcategories
    subcategories = models.ManyToManyField(SubCategory, related_name = 'entity_proposals', blank = True,
            verbose_name = _(u'Categorías'),
            limit_choices_to = {'is_active': True},
            help_text = _(u'Puedes indicar otras categorías para clasificar mejor la entidad, y que aparezca en distintas opciones de búsqueda.'))

    # Geographical info
    address_1 = models.CharField(max_length = 100, null = False, blank = True, default = '',
            verbose_name = _(u'Dirección (calle y nº)'),
            help_text = _(u'Tipo y nombre de vía y número. Ejemplos: C/ del Pez, 21; Av. de la ilustración, 145'))
    address_2 = models.CharField(max_length = 100, null = False, blank = True, default = '',
            verbose_name = _(u'Dirección (resto)'),
            help_text = _(u'Portal, piso y otros datos. Ejemplos: Escalera A, 3º izq.; Local 4 entrada posterior'))
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
    latitude = models.FloatField(max_length = 100, null = True, blank = True,
            verbose_name = _(u'Latitud'),
            help_text = _(u'Puedes introducir directamente las coordenadas (latitud) si las conoces. Ej. 41.058244'))
    longitude = models.FloatField(max_length = 100, null = True, blank = True,
            verbose_name = _(u'Longitud'),
            help_text = _(u'Puedes introducir directamente las coordenadas (longitud) si las conoces. Ej. -3.533563'))

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

    # Detailed descriptive info
    creation_year = models.IntegerField(null = True, blank = True,
            verbose_name = _(u'Año creación'),
            help_text = _(u'Año en que el colectivo u organización comenzó su actividad (introducir un nº con las cuatro cifras).'))
    legal_form = models.CharField(max_length = 100, null = False, blank = True, default = '',
            verbose_name = _(u'Forma jurídica'),
            help_text = _(u'Con qué forma jurídica concreta está registrada la entidad, si lo está.'))
    description = models.TextField(null = False, blank = True, default = '',
            verbose_name = _(u'Descripción'),
            help_text = _(u'Aquí se puede poner una descripción general, o cualquier cosa que no entre en las casillas siguientes. Si hay poca información, puede ser suficiente con rellenar esta casilla. Alternativamente, puede no ser necesaria si se han rellenado las otras con mucha información.'))
    goals = models.TextField(null = False, blank = True, default = '',
            verbose_name = _(u'Objetivo como entidad'),
            help_text = _(u'Objetivos principales de la entidad, cuál es su razón de ser; qué ofrece a sus socios, usuarios, clientes o público en general.'))
    finances = models.TextField(null = False, blank = True, default = '',
            verbose_name = _(u'Finanzas'),
            help_text = _(u'Indicar cómo gestiona el dinero (con/sin ánimo de lucro, precios de los productos si vende algo, fuentes de ingresos, modo de financiación...).'))
    social_values = models.TextField(null = False, blank = True, default = '',
            verbose_name = _(u'Valores sociales y medioambientales'),
            help_text = _(u'Justificación de por qué merece estar en este directorio, valores que aporta en función de nuestros criterios de selección, en tanto que relaciones humanas y cuidado del medio ambiente.'))
    how_to_access = models.TextField(null = False, blank = True, default = '',
            verbose_name = _(u'Forma de acceso'),
            help_text = _(u'Cómo acceder a los servicios o funciones de la entidad, horarios y lugar de contacto, condiciones de participación, venta o ditribución.'))
    networks_member = models.TextField(null = False, blank = True, default = '',
            verbose_name = _(u'Redes de las que forma parte'),
            help_text = _(u'Indicar si esta entidad está integrada en algún tipo de redes, grupo o plataforma, junto con otras entidades.'))
    networks_works_with = models.TextField(null = False, blank = True, default = '',
            verbose_name = _(u'Otras entidades con las que colabora'),
            help_text = _(u'Indicar si esta entidad trabaja en colaboración con otras entidades o redes, aún sin formar parte de ellas.'))
    ongoing_projects = models.TextField(null = False, blank = True, default = '',
            verbose_name = _(u'Proyectos en marcha'),
            help_text = _(u'Indicar, si se desea, los proyectos importantes que la entidad lleva a cabo o en los que está involucrada.'))
    needs = models.TextField(null = False, blank = True, default = '',
            verbose_name = _(u'Necesidades'),
            help_text = _(u'Indicar si la entidad tiene actualmente alguna necesidad importante que pudiera ser cubierta por otras entidades o personas externas.'))
    offerings = models.TextField(null = False, blank = True, default = '',
            verbose_name = _(u'Qué ofrece'),
            help_text = _(u'Indicar si esta entidad está en disposición de ofrecer recursos u otros elementos que puedan ser útiles a otras entidades relacionadas o personas externas; posibilidades de colaboración.'))
    additional_info = models.TextField(null = False, blank = True, default = '',
            verbose_name = _(u'Información adicional'),
            help_text = _(u'Cualquier otra información no clasificable en las casillas anteriores.'))

    class Meta:
        app_label = 'macadjan_base'
	ordering = ['-creation_date']
	verbose_name = _(u'propuesta de entidad')
	verbose_name_plural = _(u'propuestas de entidades')

    def __unicode__(self):
        return _(u'Propuesta: %s') % self.name

    def __init__(self, *args, **kwargs):
        super(EntityProposal, self).__init__(*args, **kwargs)
        self._current_status = self.status

    def save(self, update_dates = True, *args, **kwargs):
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
        super(self.__class__, self).save(*args, **kwargs)
        if self.main_subcategory and not (self.main_subcategory in self.subcategories.all()):
            self.subcategories.add(self.main_subcategory)

        if self.status != self._current_status:
            current_status = self._current_status
            self._current_status = self.status
            if current_status == EntityProposal.STATUS_PENDING \
               and self.status == EntityProposal.STATUS_ACCEPTED \
               and not self.existing_entity:
                self.generate_entity()
                self.send_mail_accepted()
            if current_status == EntityProposal.STATUS_PENDING \
               and self.status == EntityProposal.STATUS_REJECTED:
                self.send_mail_rejected()

    @property
    def categories(self):
        return Category.objects.filter(id__in = self.subcategories.values_list('category_id'))

    @property
    def active_categories(self):
        return self.categories.filter(is_active = True)

    @property
    def active_subcategories(self):
        return self.subcategories.filter(is_active = True)

    def generate_entity(self):
        entity = Entity.objects.create(
                name = self.name,
                slug = '', # will be auto generated
                alias = self.alias,
                summary = self.summary,
                is_container = False,
                contained_in = None,
                latitude = self.latitude,
                longitude = self.longitude,
                address_1 = self.address_1,
                address_2 = self.address_2,
                zipcode = self.zipcode,
                city = self.city,
                province = self.province,
                country = self.country,
                zone = self.zone,
                contact_phone_1 = self.contact_phone_1,
                contact_phone_2 = self.contact_phone_2,
                fax = self.fax,
                email = self.email,
                email_2 = self.email_2,
                web = self.web,
                web_2 = self.web_2,
                contact_person = self.contact_person,
                creation_year = self.creation_year,
                legal_form = self.legal_form,
                description = self.description,
                goals = self.goals,
                finances = self.finances,
                social_values = self.social_values,
                how_to_access = self.how_to_access,
                networks_member = self.networks_member,
                networks_works_with = self.networks_works_with,
                ongoing_projects = self.ongoing_projects,
                needs = self.needs,
                offerings = self.offerings,
                additional_info = self.additional_info,
                map_source = self.map_source,
                creation_date = None, # will be autogenerated
                modification_date = None, # will be autogenerated
                is_active = True,
                entity_type = self.entity_type,
                main_subcategory = self.main_subcategory,
            )
        for subcat in self.subcategories.all():
            entity.subcategories.add(subcat)
        self.existing_entity = entity
        self.save()
        task__geolocalize_entity.delay(self.existing_entity.pk)

    def send_mail_accepted(self):
        self.send_mail(True)

    def send_mail_rejected(self):
        self.send_mail(False)

    def send_mail(self, accepted):
        if self.proponent_email:
            current_site = Site.objects.get_current()
            site_info = current_site.site_info

            if accepted:
                email_subject = _(u'Hemos aceptado tu solicitud para dar de alta %(entity_name)s en %(website_name)s') % \
                               {'entity_name': self.name,
                                'website_name': site_info.website_name}
            else:
                email_subject = _(u'Hemos rechazado tu solicitud para dar de alta %(entity_name)s en %(website_name)s') % \
                               {'entity_name': self.name,
                                'website_name': site_info.website_name}
            email_from = settings.DEFAULT_FROM_EMAIL
            email_to = (self.proponent_email,)
            email_context = Context({
                'entity_name': self.name,
                'status_info': self.status_info,
                'website_name': site_info.website_name,
            })
            if accepted:
                from django.core.urlresolvers import reverse
                email_context.update({
                    'entity_url': 'http://' + current_site.domain +
                                  reverse('base:entity', kwargs={'entity_slug': self.existing_entity.slug})
                })
                email_template = loader.get_template('macadjan_base/email_notify_accept_to_proponent.txt')
            else:
                email_template = loader.get_template('macadjan_base/email_notify_reject_to_proponent.txt')
            email_body = email_template.render(email_context)
            email_obj = EmailMessage(
                from_email=email_from,
                subject=email_subject,
                body=email_body,
                to=email_to,
            )
            email_obj.content_subtype = 'plain'
            email_obj.send()

