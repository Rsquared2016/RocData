// Feedback
// ----------------
// model and logic for user feedback.
// same data source as user.js, but the
// appearance and behavior is different
// enough to warrant a separate module

define([], function() {
    // Constructor
    feedback = function(attr) {
        this._id = attr._id || '';
        this._rev = attr._rev || '';
        this.map = attr.map;
        this.marker = null;
        this.points = attr.points;
    };
    
    // Instance Methods
    feedback.prototype = {
        init: function() {
            // create our custom pin
            // this.marker = new feedback_pin(this);
            // this.marker.setMap(this.map.gmap);
        }
    };
    
    // Feedbacks - collection class for users
    // Constructor
    feedbacks = function(map) {
        this.map = map;
        this.all = [];
    };
    
    // Instance Methods 
    feedbacks.prototype = {
        add: function(f) {
            _.extend(f, { map: this.map });
            var model = new feedback(f).init();
            this.all.push(model);
        },
        
        addAll: function(data) {
            var self = this;
            $.each(data, function(index, f) {
                self.add(f);
            });
        },
        
        fetch: function(except, fn) {
            $.getJSON("/m/users?except=" + except, fn);
        },
        
        removeAll: function() {
            $.each(this.all, function(index, f) {
                f.destroy();
            });
            this.all.length = 0;
        }
    };
    
    // Feedback Pin
    // Custom pin overlay, similar to tweet.js
    feedback_pin = function(model) {
        this.gmap = model.map.gmap;
        this.recent = model.points[0];
        this.color = _.feedbackHealthToColor(this.recent.health);
        this.position = _.geoToLatLng(this.recent.location);
        this.canvas = null;
        this.width = 24;
        this.height = 24;
        this.zIndex = Math.floor(this.recent.health * 1000);
    };
    
    // subclass OverlayView
    feedback_pin.prototype = new google.maps.OverlayView();
    
    // Instance Methods
    _.extend(feedback_pin.prototype, {
        onAdd: function() {
            var self = this;
            // create canvas
            this.canvas = document.createElement('canvas');
            this.canvas.width = this.width;
            this.canvas.height = this.height;
            this.canvas.style.position = 'absolute';
            this.canvas.style.zIndex = this.zIndex;
            
            // draw overlay (alpha never changes here, so
            // we only have to do this once!)
            var w = this.width, h = this.height;
            var context = this.canvas.getContext('2d');
            context.globalAlpha = 0.5;
            context.beginPath();
            context.arc(w/2, h/2, w/2 - 2, 0, 2 * Math.PI, false);
            context.fillStyle = this.color;
            context.fill();
            context.lineWidth = 2;
            context.strokeStyle = "black";
            context.stroke();
            
            var panes = this.getPanes();
            $(this.canvas).appendTo(panes.overlayMouseTarget);
        },
        
        onRemove: function() {
            var context = this.canvas.getContext('2d');
            context.clearRect(0, 0, this.width, this.height);
            $(this.canvas).remove();
        },
        
        draw: function() {
            // find right position on map
            var projection = this.getProjection();
            var oldPos = projection.fromLatLngToDivPixel(this.position);
            var w = this.width, h = this.height;
            this.canvas.style.top = (oldPos.y - h / 2) + 'px';
            this.canvas.style.left = (oldPos.x - w / 2) + 'px';
        }
    });
    
    return {
        Model: feedback,
        Collection: feedbacks,
        Overlay: feedback_pin
    };
});