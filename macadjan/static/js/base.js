/* Author:
    RedDelicious
    Company: Kaleidos Open Source
*/

/* gettext dummy wrapper if not exists */

if (window.gettext === undefined) {
    window.gettext = function(text) {
        return text;
    };
}

if (window.interpolate === undefined) {
    window.interpolate = function(fmt, obj, named) {
        if (named) {
            return fmt.replace(/%\(\w+\)s/g, function(match){return String(obj[match.slice(2,-2)])});
        } else {
            return fmt.replace(/%s/g, function(match){return String(obj.shift())});
        }
    };
}

$(document).ajaxSend(function(event, xhr, settings) {
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    function sameOrigin(url) {
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            !('/^(\/\/|http:|https:).*\/'.test(url)); // or any other URL that isn't scheme relative or absolute i.e relative.
    }

    function safeMethod(method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    if (!safeMethod(settings.type) && sameOrigin(settings.url)) {
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    }
});


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

Macadjan.Map = Backbone.View.extend({
    el: $("#map-block"),

    events: {},

    initialize: function() {
        _.bindAll(this);

        this.mapArgs = {
            projection: new OpenLayers.Projection('EPSG:4326'),
            controls: [
                new OpenLayers.Control.Navigation(),
                new OpenLayers.Control.LayerSwitcher(),
                new OpenLayers.Control.PanZoomBar(),
            ],
            maxExtent: this.parseBounds(),
            numZoomLevels: this.parseZoomLevels(),
            units:this.parseUnits(),
            maxResolution: this.parseMaxResolution()
        };
        this.map = new OpenLayers.Map(this.$el.attr('id'), this.mapArgs);

        this.osm = this.createOsmLayer();
        this.map.addLayer(this.osm);

        // Center map to initial coords
        this.centerMap();

        // Create points layer
        this.pointsLayer = this.createPointsLayer();
        this.map.addLayer(this.pointsLayer);

        // Create select control
        this.selectControl = this.createSelectControl(this.pointsLayer);
        this.map.addControl(this.selectControl);

        this.pointsLayer.events.on({
            "featureselected": this.onFeatureSelect,
            "featureunselected": this.onFeatureUnselect,
        });
    },

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

    onFeatureSelect: function(evt) {
        var feature = evt.feature;
        var content;

        if (!feature.cluster) {
            content = feature.attributes.title + '<br/>' + feature.attributes.description;
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
        map.addPopup(popup, true);
    },

    onFeatureUnselect: function(evt) {
        var feature = evt.feature;
        if (feature.popup) {
            popup.feature = null;
            map.removePopup(feature.popup);
            feature.popup.destroy();
            feature.popup = null;
        }
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

    createOsmLayer: function() {
        return new OpenLayers.Layer.OSM({
            transitionEffect: 'resize'
        })
    },

    createPointsLayer: function() {
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
            params: {'features': '|||'},
            format: new OpenLayers.Format.Text(),
        });
        
        this.style = new OpenLayers.Style({
            pointRadius: "${radius}",
            //fillColor: "#cc6633",
            fillColor: "#cc1111",
            fillOpacity: 0.9,
            //strokeColor: "#ffcc66",
            strokeColor: "#cc1111",
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

        var pointsLayerArgs = {
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

        return new OpenLayers.Layer.Vector("POIs", pointsLayerArgs);
    },

    createSelectControl: function(layer) {
        return new OpenLayers.Control.SelectFeature(layer);
    },

    refresh: function(categoryId, subCategoryId, keywords) {
        Macadjan.map.protocol.params['features'] = (categoryId || '') + '|' + (subCategoryId || '') + '|' + keywords;
        Macadjan.map.refreshStrategy.refresh();
    },
});

Macadjan.map = new Macadjan.Map();

Macadjan.MainView = Backbone.View.extend({
    el: $("body"),

    events: {
        'change #id_category': 'onChangeCategory',
        'change #id_subcategory': 'onChangeSubCategory',
        'click #id_keywords_submit': 'onClickKeywords',
    },

    initialize: function() {
        _.bindAll(this);
        this.container = this.$(".main-container");

        Macadjan.categories.on('reset', this.onResetCategories);
        Macadjan.subCategories.on('reset', this.onResetSubCategories);
    },

    onResetCategories: function() {
        var self = this;
        var selectCategory = this.$('#id_category');
        selectCategory.empty();
        var option = self.make("option", {'value': ''}, 'Selecciona uno');
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
            var option = self.make("option", {'value': ''}, 'Selecciona uno');
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

        this.refreshMap();
    },

    onChangeSubCategory: function(evt) {
        var self = this;

        var selectCategory = this.$('#id_category');
        var selectSubCategory = this.$('#id_subcategory');
        var currentCategoryId = selectCategory.val();
        var currentSubCategoryId = selectSubCategory.val();

        this.refreshMap();
    },

    onClickKeywords: function(evt) {
        this.refreshMap();
    },

    refreshMap: function() {
        var self = this;

        var selectCategory = this.$('#id_category');
        var selectSubCategory = this.$('#id_subcategory');
        var inputKeywords = this.$('#id_keywords');

        var currentCategoryId = selectCategory.val();
        var currentSubCategoryId = selectSubCategory.val();
        var currentKeywords = inputKeywords.val();

        Macadjan.map.refresh(currentCategoryId, currentSubCategoryId, currentKeywords);
    },
});

Macadjan.main = new Macadjan.MainView();

