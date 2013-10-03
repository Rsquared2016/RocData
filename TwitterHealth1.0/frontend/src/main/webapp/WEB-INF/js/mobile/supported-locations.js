define(["../common/util"], function(util) {
    
    var locations = {
        // Boston
        boston: {
            lat: 42.3644,
            lng: -71.059,
            radius: 50
        },
        
        // LA
        los_angeles: {
            lat: 33.995,
            lng: -118.063,
            radius: 100
        },
        
        // London
        london: {
            lat: 51.514,
            lng: -0.122,
            radius: 100
        },
        
        // NYC
        new_york_city: {
            lat: 40.716667,
            lng: -74.00,
            radius: 100
        },
        
        // Seattle
        seattle: {
            lat: 47.577,
            lng: -122.229,
            radius: 100
        },
        
        // SF
        san_francisco: {
            lat: 37.566,
            lng: -122.327,
            radius: 100
        },
        
        // Rochester+Buffalo+Toronto
        roc_buffalo_toronto: {
            lat: 43.164,
            lng: -77.610,
            radius: 170
        },
    };
    
    var getNearest = function(location) {
        // earth circumference
        var nearestDistance = 40075000;
        var nearestLocation = null;
        for ( var name in locations) {
            var loc = locations[name];
            var lat = loc.lat;
            var lng = loc.lng;
            var radius = loc.radius;
            var distance = util.calcDistance(location.lat, location.lng, lat, lng)
                - radius * 1000;
            if (distance < nearestDistance) {
                nearestDistance = distance;
                nearestLocation = loc;
            }
        }
        
        return {
            lat: nearestLocation.lat,
            lng: nearestLocation.lng
        };
    };
    
    return {
        getNearest: getNearest
    };
    
});
