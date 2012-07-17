
/* Global macadjan  module namespace. */

var Macadjan = {}

Macadjan.Category = Backbone.Model.extend({});
Macadjan.SubCategory = Backbone.Model.extend({});

Macadjan.CategoryCollection = Backbone.Collection.extend({
    model: Macadjan.Category
});

Macadjan.SubCategoryCollection = Backbone.Collection.extend({
    model: Macadjan.SubCategory
});

Macadjan.categories = new Macadjan.CategoryCollection();
Macadjan.subCategories = new Macadjan.SubCategoryCollection();


/* Map block view. */

Macadjan.MapView = Backbone.View.extend({
    el: $("#map-block"),

    events: {},

    initialize: function() {
        _.bindAll(this);

        this.map = this.createMap();

        this.osm = this.createOSMLayer();
        this.map.addLayer(this.osm);

        this.poiLayer = this.createPOILayer();
        this.map.addLayer(this.poiLayer);

        this.selectControl = this.createSelectControl(this.poiLayer);
        this.map.addControl(this.selectControl);
        this.selectControl.activate();
        this.poiLayer.events.on({
            "featureselected": this.onFeatureSelect,
            "featureunselected": this.onFeatureUnselect,
        });

        this.centerMap();
    },

    createMap: function() {
        var mapArgs = {
            projection: new OpenLayers.Projection('EPSG:4326'),
            controls: [
                new OpenLayers.Control.Navigation(),
                new OpenLayers.Control.PanZoomBar(),
            ],
            maxExtent: this.parseBounds(),
            numZoomLevels: this.parseZoomLevels(),
            units:this.parseUnits(),
            maxResolution: this.parseMaxResolution()
        };
        return new OpenLayers.Map(this.$el.attr('id'), mapArgs);
    },

    createOSMLayer: function() {
        var layer = new OpenLayers.Layer.OSM();
        layer.transitionEffect = 'resize';
        return layer;
    },

    createPOILayer: function() {
        this.bboxStrategy = new OpenLayers.Strategy.BBOX();
        this.clusterStrategy = new OpenLayers.Strategy.Cluster({
            distance: 50,
            threshold: 1
        });
        this.refreshStrategy = new OpenLayers.Strategy.Refresh({
            force: true,
            active: true,
        });

        this.protocol = new OpenLayers.Protocol.HTTP({
            url: this.$el.data('api-url'),
            params: {'features': this.parseFilter()},
            format: new OpenLayers.Format.Text(),
        });

        this.style = new OpenLayers.Style({
            pointRadius: "${radius}",
            fillColor: "#ff9909",
            //fillColor: "#cc1111",
            fillOpacity: 0.9,
            strokeColor: "#f15800",
            //strokeColor: "#cc1111",
            strokeWidth: 10,
            strokeOpacity: 0.4,
            label: "${count}",
            fontColor: "#ffffff",
        },{
            context: {
                radius: function(feature) {
                    return Math.min(Math.max(feature.attributes.count, 10), 50);
                },
                count: function(feature) {
                    return feature.attributes.count;
                }
            }
        });

        var poiLayerArgs = {
            strategies: [
                this.bboxStrategy,
                this.clusterStrategy,
                this.refreshStrategy,
            ],
            protocol: this.protocol,
             styleMap: new OpenLayers.StyleMap({
                 "default": this.style,
                 "select": {
                     fillColor: "#8aeeef",
                     strokeColor: "#32a8a9"
                 }
             })
        };

        return new OpenLayers.Layer.Vector("POIs", poiLayerArgs);
    },

    createSelectControl: function(layer) {
        return new OpenLayers.Control.SelectFeature(layer);
    },

    centerMap: function() {
        var initialLon = this.$el.data('initial-lon');
        var initialLat = this.$el.data('initial-lat');
        var initialZoom = this.$el.data('initial-zoom');

        this.map.setCenter(new OpenLayers.LonLat(initialLon, initialLat).transform(
            new OpenLayers.Projection("EPSG:4326"), // transform from WGS 1984
            new OpenLayers.Projection("EPSG:900913") // to Spherical Mercator Projection
        ), initialZoom);
    },

    zoomTo: function(lon, lat, zoom) {
        /*
        this.map.events.register('moveend', this.map, this.pru);
        this.map.events.register('zoomend', this.map, this.pru);
        */

        this.map.setCenter(new OpenLayers.LonLat(lon, lat).transform(
            new OpenLayers.Projection("EPSG:4326"), // transform from WGS 1984
            new OpenLayers.Projection("EPSG:900913") // to Spherical Mercator Projection
        ), zoom);
    },

    /*
    pru: function(evt) {
        var layer = this.map.layers['POIs'];
        alert('kongo');

        this.map.events.unregister('moveend', this.map, this.pru);
        this.map.events.unregister('zoomend', this.map, this.pru);
    },
    */

    parseBounds: function() {
        var b = {
            "left": this.$el.data('map-bounds-left') || -20037508.34,
            "right": this.$el.data('map-bounds-right') || 20037508.34,
            "top": this.$el.data('map-bounds-top') || 20037508.34,
            "bottom": this.$el.data('map-bounds-bottom') || -20037508.34
        };

        return new OpenLayers.Bounds(b['left'], b['bottom'], b['right'], b['top']);
    },

    parseZoomLevels: function() {
        return 18;
    },

    parseUnits: function() {
        return "meters";
    },

    parseMaxResolution: function() {
        return 156543;
    },

    parseFilter: function() {
        var cat = this.$el.data('initial-cat') || '';
        var subcat = this.$el.data('initial-subcat') || '';
        var keywords = this.$el.data('initial-keywords') || '';
        return cat + '|' + subcat + '|' + keywords
    },

    onFeatureSelect: function(evt) {
        var feature = evt.feature;
        var content;

        if (!feature.cluster) {
            content = feature.attributes.title + '<br/>' + feature.attributes.description;
        } else if (feature.cluster.length == 1) {
            content = feature.cluster[0].attributes.title + '<br/>' + feature.cluster[0].attributes.description;
        } else {
            content = '';
            var length = Math.min(feature.cluster.length, 50);
            for (var c = 0; c < length; c++) {
                content += feature.cluster[c].attributes.title + '<br/>';
            }
            if (length < feature.cluster.length) {
                content += '(...)';
            }
        }
        var self = this;

        var popup = new OpenLayers.Popup.FramedCloud('featurePopup',
            feature.geometry.getBounds().getCenterLonLat(),
            new OpenLayers.Size(300, 100),
            content, null, true,
            function(evt) {
                var feature = this.feature;
                if (feature.layer) {
                    self.selectControl.unselect(feature);
                } else {
                    this.destroy();
                }
            }
        );

        popup.maxSize = new OpenLayers.Size(500, 300);
        feature.popup = popup;
        popup.feature = feature;
        this.map.addPopup(popup, true);
    },

    onFeatureUnselect: function(evt) {
        var feature = evt.feature;
        if (feature.popup) {
            feature.popup.feature = null;
            this.map.removePopup(feature.popup);
            feature.popup.destroy();
            feature.popup = null;
        }
    },

    refresh: function() {
        this.protocol.params['features'] = this.parseFilter();
        this.refreshStrategy.refresh();
    },
});

Macadjan.mapView = new Macadjan.MapView();


/* Search box view. */

Macadjan.MapPageView = Backbone.View.extend({
    el: $("#map-page"),

    events: {
        'change #id_category': 'onChangeCategory',
        'change #id_subcategory': 'onChangeSubCategory',
        'click #id_keywords_submit': 'onClickKeywords',
        'click #list-block .with-point strong': 'onClickEntityNameWithPoint',
        'click #list-block .without-point strong': 'onClickEntityNameWithoutPoint',
    },

    initialize: function() {
        _.bindAll(this);

        Macadjan.categories.on('reset', this.onResetCategories);
        Macadjan.subCategories.on('reset', this.onResetSubCategories);

        this.loadList();
    },

    onResetCategories: function() {
        var self = this;

        var selectCategory = this.$('#id_category');
        selectCategory.empty();

        var option = self.make("option", {'value': ''}, 'Todos los temas');
        selectCategory.append(option);

        Macadjan.categories.each(function(item) {
            var option = self.make("option", {'value': item.get('id')}, item.get('name'));
            selectCategory.append(option);
        })
    },

    onResetSubCategories: function() {
        var self = this;

        var selectSubCategory = this.$('#id_subcategory');
        selectSubCategory.empty();
        selectSubCategory.hide();
    },

    getCategory: function() {
    },

    onChangeCategory: function(evt) {
        var self = this;

        var selectCategory = this.$('#id_category');
        var selectSubCategory = this.$('#id_subcategory');
        var currentCategoryId = selectCategory.val();

        if (!currentCategoryId) {
            selectSubCategory.empty();
            selectSubCategory.hide();
        } else {
            selectSubCategory.empty();
            var option = self.make("option", {'value': ''}, 'Todos los temas');
            selectSubCategory.append(option);

            var subcategories = Macadjan.subCategories.filter(
                function(item){
                    return item.get('category_id') == currentCategoryId
                }
            );
            _.each(subcategories, function(item) {
                var option = self.make("option", {'value': item.get('id')}, item.get('name'));
                selectSubCategory.append(option);
            })

            selectSubCategory.show();
        }

        this.$el.data('initial-cat', currentCategoryId);
        this.$el.data('initial-subcat', '');
        this.$('#map-block').data('initial-cat', currentCategoryId);
        this.$('#map-block').data('initial-subcat', '');
        this.refresh();
    },

    onChangeSubCategory: function(evt) {
        var selectSubCategory = this.$('#id_subcategory');
        var currentSubCategoryId = selectSubCategory.val();

        this.$el.data('initial-subcat', currentSubCategoryId);
        this.$('#map-block').data('initial-subcat', currentSubCategoryId);
        this.refresh();
    },

    onClickKeywords: function(evt) {
        var inputKeywords = this.$('#id_keywords');
        var currentKeywords = inputKeywords.val();

        this.$el.data('initial-keywords', currentKeywords.trim());
        this.$('#map-block').data('initial-keywords', currentKeywords);
        this.refresh();
    },

    onClickEntityNameWithPoint: function(event) {
        var target = $(event.currentTarget);
        var lon = target.data('entity-lon');
        var lat = target.data('entity-lat');
        Macadjan.mapView.zoomTo(lon, lat, 16);
    },

    onClickEntityNameWithoutPoint: function(event) {
        var target = $(event.currentTarget);
        var url = target.data('entity-url');
        window.open(url);
    },

    refresh: function() {
        this.loadList();
        Macadjan.mapView.refresh();
    },

    loadList: function() {
        var self = this;

        var cat = this.$el.data('initial-cat');
        var category = Macadjan.categories.find(function(item) {return item.get('id') == cat;});
        var subCat = this.$el.data('initial-subcat');
        var subCategory = Macadjan.subCategories.find(function(item) {return item.get('id') == subCat;});
        var keywords = this.$el.data('initial-keywords');

        var categoryBlock = this.$('#id-category-block');
        var categoryHeader = this.$('#id-category-header');
        var categoryTitle = this.$('#id-category-title');
        var categoryDescription = this.$('#id-category-description');

        var filterName, filterTitle, filterDescription;
        if (subCategory) {
            filterName = subCategory.get('name');
            filterDescription = subCategory.get('description');
        } else if (category) {
            filterName = category.get('name');
            filterDescription = category.get('description');
        } else {
            filterName = 'Todos los temas';
            filterDescription = '';
        }
        if (keywords) {
            if (keywords.split(' ').length > 1) {
                filterLine = filterName.toLowerCase() + ' y las palabras ' + keywords;
            } else {
                filterLine = filterName.toLowerCase() + ' y la palabra ' + keywords;
            }
        } else {
            filterLine = filterName.toLowerCase();
        }
        categoryHeader.text(filterLine);
        categoryTitle.text(filterName);
        categoryDescription.text(filterDescription);

        $.get(
            this.$el.data('entity-list-url'),
            {
                features: (cat || '') + '|' + (subCat || '') + '|' + keywords,
                bbox: '',
            },
            function(data) {
                var listBlock = self.$('#list-block');
                var categoryBlock = self.$('#id-category-block');
                listBlock.html(data);
                var categoryBlockHeight = categoryBlock.height() + 30;  // 30 is the padding of the blocks
                listBlock.height(600 - categoryBlockHeight);
            }
        );
    },
});

Macadjan.mapPage = new Macadjan.MapPageView();

