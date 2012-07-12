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

    initializeControls: function() {
        this.navigationControl = new OpenLayers.Control.Navigation();
        this.layerSwitcherControl = new OpenLayers.Control.LayerSwitcher();
        this.panZoomControl = new OpenLayers.Control.PanZoomBar();
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

    initialize: function() {
        _.bindAll(this);

        this.initializeControls();
        this.mapInitial = {
            projection: new OpenLayers.Projection('EPSG:4326'),
            controls: [
                this.navigationControl,
                this.layerSwitcherControl,
                this.panZoomControl
            ],
            maxExtent: this.parseBounds(),
            numZoomLevels: this.parseZoomLevels(),
            units:this.parseUnits(),
            maxResolution: this.parseMaxResolution()
        };

        this.map = new OpenLayers.Map(this.$el.attr('id'), this.mapInitial);

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
    }
});

Macadjan.map = new Macadjan.Map();

Macadjan.MainView = Backbone.View.extend({
    el: $("body"),

    events: {},

    initialize: function() {
        _.bindAll(this);
        this.container = this.$(".main-container");
    },
});

Macadjan.main = new Macadjan.MainView();

