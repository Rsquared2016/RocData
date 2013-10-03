function DistanceHeatmap(name, options, dataSource) {
    this.name = name;
    this.radius = options.radius;
    this.color = options.color;
    this.markers = {};
    this.dataSource = dataSource;
}

DistanceHeatmap.prototype.draw = function(context) {

    var data = this.dataSource.data;
    if (!data) {
        log.info("dataSource for " + this.name
                + " not initialized, skipping...");
        return;
    }

    var map = context.map;
    var projection = context.projection;
    var bounds = map.getBounds();
    var sw = projection.fromLatLngToDivPixel(bounds.getSouthWest());
    var ne = projection.fromLatLngToDivPixel(bounds.getNorthEast());
    var h = sw.y - ne.y, w = ne.x - sw.x;
    var ctx = context.canvasCtx;
    var i = h, j = w;
    var point = {};
    var latLng;
    var radius = this.radius, min;
    var newData = filterData(data, bounds);
    var c = this.color;
    log.info(this.name + " data size: " + data.length);
    log.info(this.name + " filtered data size: " + newData.length);
    log.info(this.name + "'s radius: " + radius);

    while ((i -= 3) > 0) {
        while ((j -= 3) > 0) {
            point.x = j;
            point.y = i;
            latLng = projection.fromContainerPixelToLatLng(point);
            min = minDistance(latLng.lat(), latLng.lng(), newData);
            ctx.fillStyle = "rgba(" + c.r + "," + c.g + "," + c.b + "," + 255
                    * Math.min(1.0, min / radius) + ")";
            ctx.fillRect(j, i, 3, 3);
        }
        j = w;
    }

    log.info("done");
};

DistanceHeatmap.prototype.addMarkers = function(map, data, type) {
    log.info("adding markers of type " + type);
    var markers;
    if (!this.markers[type]) {
        markers = {
            data : [],
            visible : true
        };
        this.markers[type] = markers;
    } else
        markers = this.markers[type];

    var dlen = data.length;
    while (dlen--) {
        var geo = data[dlen].geo_location;
        var latLng = geoToLatLng(geo);
        var marker = new google.maps.Marker({
            position : latLng,
            map : map,
            title : data[dlen].name
        });
        markers.data.push(marker);
    }
    log.info("markers of type " + type + " added");
};

DistanceHeatmap.prototype.toggleMarkers = function(type) {
    log.info("toggle markers of type " + type);
    var markers = this.markers[type];

    if (!markers)
        return;

    var len = markers.data.length;
    while (len--) {
        markers.data[len].setVisible(!markers.visible);
    }
    markers.visible = !markers.visible;
    log.info("markers of type " + type + " toggled");
};

DistanceHeatmap.prototype.hasMarkers = function(type) {
    return this.markers[type] ? true : false;
};

function minDistance(lat, lng, data) {
    var min = 1000000, dlen = data.length, dist, geo;
    while (dlen--) {
        geo = data[dlen].geo_location;
        dist = calcDistanceOptimized(lat, lng, geo.lat, geo.lng);
        if (min > dist)
            min = dist;
    }
    return min;
}

function filterData(data, bounds) {
    var newData = [], dlen = data.length, geo, latLng;
    while (dlen--) {
        geo = data[dlen].geo_location;
        latLng = geoToLatLng(geo);
        if (bounds.contains(latLng)) {
            newData.push(data[dlen]);
        }
    }
    return newData;
}

function geoToLatLng(geo) {
    return new google.maps.LatLng(geo.lat, geo.lng, false);
}

function calcDistance(lat1, lng1, lat2, lng2) {
    var nauticalMilePerLat = 60.00721, nauticalMilePerLongitude = 60.10793, rad = Math.PI / 180.0, milesPerNauticalMile = 1.15078;

    var yDistance = (lat2 - lat1) * nauticalMilePerLat;
    var xDistance = (Math.cos(lat1 * rad) + Math.cos(lat2 * rad))
            * (lng2 - lng1) * (nauticalMilePerLongitude / 2);

    var distance = Math.sqrt(yDistance * yDistance + xDistance * xDistance);

    return distance * milesPerNauticalMile * 1609.344;
}

function calcDistanceOptimized(lat1, lng1, lat2, lng2) {
    var rad = 0.017453292519943;
    var yDistance = (lat2 - lat1) * 60.00721;
    var xDistance = (Math.cos(lat1 * rad) + Math.cos(lat2 * rad))
            * (lng2 - lng1) * 30.053965;
    var distance = Math.sqrt(yDistance * yDistance + xDistance * xDistance);
    return distance * 1852.00088832;
}
