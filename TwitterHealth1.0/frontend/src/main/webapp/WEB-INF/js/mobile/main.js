// entry point of the app 

require(
    ["map", "../common/options", "../common/util"],
    function(Map, options, util) {
        // mixin globals
        _.mixin(util);
        var update_timer = new Date().getTime();
        var start = {
            location: {
                // some invalid coordinates as a default
                lat: 190.0,
                lng: 190.0
            }
        };
        
        // create map
        if (navigator.geolocation) {
            var map = null;
            
            // try to get cookie that IDs user
            var uid = _.getCookie("mobile-user-id-fountin");
            if(!uid) {
                uid = _.generateUniqueUserId();
                _.setCookie("mobile-user-id-fountin", uid);
            }
            
            // success callback for static: get user location, create map
            successStatic = function(position) {
                start.location.lat = position.coords.latitude;
                start.location.lng = position.coords.longitude;
                if (_.isValidLocation(start.location)) {
                    map = new Map("map_canvas", options.mapStyle, start.location, uid);
                    map.init();
                }
            };
            
            // success callback for dynamic: periodically updatel location
            successDynamic = function(position) {
                if (!map) {
                    start.location.lat = position.coords.latitude;
                    start.location.lng = position.coords.longitude;
                    if (_.isValidLocation(start.location)) {
                        map = new Map("map_canvas", options.mapStyle, start.location);
                        map.init();
                    }
                } else {
                    var now = new Date().getTime();
                    // only update every 30 seconds
                    if (now - update_timer >= 30000) {
                        var loc = {
                            lat: position.coords.latitude,
                            lng: position.coords.longitude
                        };
                        map.update({
                            center: _.geoToLatLng(loc)
                        });
                        update_timer = now;
                    }
                }
            };
            
            // failure callback: report error
            failure = function(error) {
                switch (error.code) {
                case error.TIMEOUT:
                    error = 'Sorry it\'s taking too long to try and find your location...';
                    break;
                case error.POSITION_UNAVAILABLE:
                    error = 'Sorry, this browser either doesn\'t support geolocation or your gps isn\'t turned on.';
                    break;
                case error.PERMISSION_DENIED:
                    error = 'We weren\'t allowed to get your exact location, please check your permission settings if this device has GPS';
                    break;
                case error.UNKNOWN_ERROR:
                    error = 'Sorry, i have no clue why this wouldn\'t work.';
                    break;
                }
                $('#message').removeClass("alert-message").addClass("alert-error");
                log.info(error);
                map = new Map("map_canvas", options.mapStyle, null);
                map.init();
            };
            
            useragent = navigator.userAgent; // TODO: cache this
            // allow iPhone or Android to track movement, or let other
            // geolocation-capable browsers get a static position
            if (useragent.indexOf('iPhone') !== -1 || useragent.indexOf('Android') !== -1) {
                navigator.geolocation.watchPosition(successDynamic, failure, {
                    enableHighAccuracy: true,
                    maximumAge: 30000,
                    timeout: 27000
                });
            } else {
                navigator.geolocation.getCurrentPosition(successStatic, failure, {
                    enableHighAccuracy: true,
                    maximumAge: 300000
                });
            }
        }
    });
