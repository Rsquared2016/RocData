// Map
// ----------------
// model and logic for the map
define(["list", "tweet", "report", "controls", "supported-locations", "user"], function(List,
    Tweet, Report, Controls, supportedLocations, User) {
    // Constructor
    map = function(element, options, start, user_id) {
        this.element = document.getElementById(element);
        this.options = options;
        this.start = start ? _.geoToLatLng(supportedLocations.getNearest(start)) : _
            .geoToLatLng(_.sfDefault());
        this.center = this.start;
        this.gmap = new google.maps.Map(this.element, this.options);
        this.user_id = user_id;
        this.bounds = null;
        this.tweets = new Tweet.Collection(this);
        this.list = null;
        this.controls = {};
        this.health_risk = 0.0;
        this.radius = new HealthRadius(this);
        this.user = start ? new User(this, start) : null;
        this.report = null;
    };
    
    // Instance Methods
    map.prototype = {
        // init: asynchronous initialization (i.e. we had to wait on
        // some event to get certain data)
        init: function() {
            var self = this;
            
            // get initial bounds
            this.bounds = this.gmap.getBounds();
            
            // center map, place user marker
            var zoom = this.gmap.getZoom();
            this.gmap.setCenter(this.center);
            this.gmap.setZoom(zoom);
            
            // add bootstrapped data if available
            if (window.bootstrap) {
                var tweetsCollect = [];
                // post data to Mr. Sadilek and receive data in kind
                // (one at a time for now)
                $.each(window.bootstrap.tweets, function(i, t) {
                    tweetsCollect.push(t);
                    if ((i + 1) % 50 == 0 || i + 1 >= window.bootstrap.tweets.length) {
                        $.ajax({
                            url: '/m/data',
                            type: "POST",
                            data: JSON.stringify({
                                "tweets": tweetsCollect
                            }),
                            contentType: "application/json",
                            dataType: "application/json",
                            async: true,
                            success: function(data, status) {
                                data = $.parseJSON(data);
                                // self.health_risk = data.health_risk;
                                self.tweets.addAll(data.tweets);
                            },
                            error: function(jqxhr, status) {
                                log.info(status);
                            }
                        });
                        tweetsCollect = [];
                    }
                });
            }
            
            google.maps.event.addListener(self.gmap, "idle", function(event) {
                self.panned();
            });
            
            google.maps.event.addListener(self.gmap, "center_changed", function(event) {
                self.radius.risk = null;
                self.radius.draw();
            });
            
            _.setLinkWithIcon($('a#view_toggle_link'), 'List', 'icon-list');
            $('a#view_toggle_link').unbind('click').bind('click', function(event) {
                if (self.list)
                    self.list.destroy();
                self.tweets.sortByHealth();
                self.list = new List({
                    map: self,
                    center: self.center,
                    health_risk: self.health_risk,
                    tweets: self.tweets.all
                });
                self.list.show();
            });
            
            // TODO Fix this so it isn't relying on Google Maps DOM structure.
            // Set zoom controls below overlay
            google.maps.event.addListener(self.gmap, 'tilesloaded', function() {
                var controlClass;
                if ((navigator.platform.indexOf("iPhone") != -1)
                    || (navigator.platform.indexOf("iPad") != -1)) {
                    controlClass = 'ios-google-maps-controls';
                } else {
                    controlClass = 'google-maps-controls';
                }
                $('div.gmnoprint').last().addClass(controlClass);
            });
            
            this.radius.draw();
            
            // Set map overlay risk classification text
            _.setHealthClassification($('#current_health_risk'), this.health_risk);
            
            // setup user
            if (self.user)
                self.user.init();

            // setup report tab click handler
            var report = new Report($('#report_tab_wrapper'), this.user);
            report.init();
        },
        
        // update: change parameters
        update: function(attr) {
            // if center changed, reposition map and move user
            if (attr.center && !attr.center.equals(this.center)) {
                if (_.isInBounds(attr.center, ["nyc", "sf"]))
                    this.gmap.setCenter(attr.center);
            }
            // if health score changed, update score and save new score
            // point
            
            // update health risk radius
            this.radius.draw();
        },
        
        // panned: what to do when the map is done being moved
        panned: function() {
            var self = this;
            var tweets = this.tweets;
            this.bounds = this.gmap.getBounds();
            var ne = this.bounds.getNorthEast();
            var sw = this.bounds.getSouthWest();
            var left = sw.lng();
            var right = ne.lng();
            var top = ne.lat();
            var bottom = sw.lat();
            this.center = this.gmap.getCenter();
            var user_lat = null;
            var user_lon = null;
            if (self.user) {
                user_lat = self.user.location.lat();
                user_lon = self.user.location.lng();
            }
            this.tweets.fetchByGeo(left, bottom, right, top, user_lat, user_lon,
                function(data) {
                    self.health_risk = data.health_risk;
                    // remove old tweets and list view
                    tweets.removeAll();
                    // add new tweets and list view
                    tweets.addAll(data.tweets);
                    
                    self.radius.risk = data.health_risk;
                    
                    // update map overlay risk classification text && radius
                    self.radius.draw();
                    _
                        .setHealthClassification($('#current_health_risk'),
                            self.health_risk);
                });
        },
        
        // show: show map, hide others
        show: function() {
            var self = this;
            $('.map-view').show();
            if (this.list)
                this.list.hide();
            _.setLinkWithIcon($('a#view_toggle_link'), 'List', 'icon-list');
            $('a#view_toggle_link').unbind('click').bind('click', function(event) {
                if (self.list)
                    self.list.destroy();
                self.list = new List({
                    map: self,
                    center: self.center,
                    health_risk: self.health_risk,
                    tweets: self.tweets.all
                });
                self.list.show();
            });
            $('#map_overlay_tweet_wrapper').show();
        },
        
        // hide: hide this view
        hide: function() {
            $('.map-view').hide();
        },
        
        // isOutside: returns true if we are displaying NYC but are in another
        // location
        isOutside: function() {
            return !this.center.equals(this.start)
                && this.center.equals(_.geoToLatLng(_.nycDefault()));
        }
    };
    
    // HealthRadius - a google maps overlay for the health risk radius
    // Constructor
    HealthRadius = function(map) {
        this._map = map;
        this.map = map.gmap;
        this.setMap(map.gmap);
    };
    
    // subclass OverlayView
    HealthRadius.prototype = new google.maps.OverlayView();
    
    // Instance Methods
    _.extend(HealthRadius.prototype, {
        onAdd: function() {
            // create canvas
            this.canvas = document.createElement('canvas');
            this.canvas.width = this.size;
            this.canvas.height = this.size;
            this.canvas.style.position = 'absolute';
            this.canvas.style.zIndex = this.zIndex;
            var panes = this.getPanes();
            $(this.canvas).appendTo(panes.overlayShadow);
        },
        
        onRemove: function() {
            var context = this.canvas.getContext('2d');
            context.clearRect(0, 0, context.width, context.height);
            $(this.canvas).remove();
        },
        
        draw: function() {
            var map = this._map;
            var risk = this.risk;
            var num = map.gmap.getZoom() - 4;
            this.size = Math.pow(2, num);
            var color = (risk != null) ? _.healthRiskToColor(map.health_risk) : "#AAAAA";
            
            // find right position on map
            var projection = this.getProjection();
            if (!projection)
                return;
            var center = projection.fromLatLngToDivPixel(map.gmap.getCenter());
            var w = this.size;
            var h = this.size;
            this.canvas.style.top = (center.y - h / 2) + 'px';
            this.canvas.style.left = (center.x - w / 2) + 'px';
            this.canvas.width = w;
            this.canvas.height = h;
            
            // draw overlay (alpha never changes here, so
            // we only have to do this once!)
            var context = this.canvas.getContext('2d');
            context.clearRect(0, 0, context.width, context.height);
            context.globalAlpha = 0.5;
            context.beginPath();
            context.arc(w / 2, h / 2, Math.max(1, w / 2 - 3), 0, 2 * Math.PI, false);
            context.fillStyle = color;
            context.fill();
            context.lineWidth = 2;
            context.strokeStyle = color;
            context.stroke();
        }
    });
    
    return map;
});
