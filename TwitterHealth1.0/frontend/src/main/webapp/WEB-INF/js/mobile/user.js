// User
// ----------------
// model and logic for a user of the site.
// right now, just a location and a pin, but
// perhaps there will be more stuff in future?
// (for now this is effectively a singleton)

define([], function() {
    // Constructor
    user = function(map, location) {
    	this._id = map.user_id;
        this._rev = '';
        this.map = map;
        this.location = _.geoToLatLng(location);
        this.marker = null;
    };
    
    // Instance Methods
    user.prototype = {
        init: function() {
            if (!this.location)
                return;
            
            // define our custom marker image
            var image = new google.maps.MarkerImage(
                '/css/images/bluedot_retina.png',
                null, // size
                null, // origin
                new google.maps.Point( 8, 8 ), // anchor (move to center of marker)
                new google.maps.Size( 17, 17 ) // scaled size (required for Retina display icon)
            );

            // then create the new marker
            this.marker = new google.maps.Marker({
                flat: true,
                icon: image,
                map: this.map.gmap,
                optimized: false,
                position: this.location,
                title: 'You',
                visible: true
            });
        }
    };
    
    return user;
});