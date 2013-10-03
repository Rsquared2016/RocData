/* 
 * heatmap.js GMaps overlay
 *
 * Copyright (c) 2011, Patrick Wied (http://www.patrick-wied.at)
 * Dual-licensed under the MIT (http://www.opensource.org/licenses/mit-license.php)
 * and the Beerware (http://en.wikipedia.org/wiki/Beerware) license.
 */

function HeatmapOverlay(map, cfg) {
    this.heatmap = null;
    this.conf = cfg;
    this.setMap(map);
    this.rtree = new RTree();
    this.isEmpty = true;
    this.suppressDraw = true;
    this.taskCallback = cfg.taskCallback;
    this.skipDrawOnIdleOnce = true;
    this.cityBounds = cfg.cityBounds;
};

HeatmapOverlay.prototype = new google.maps.OverlayView();

HeatmapOverlay.prototype.onAdd = function() {
    var panes = this.getPanes();
    var w = this.getMap().getDiv().clientWidth;
    var h = this.getMap().getDiv().clientHeight;
    var el = document.createElement("div");
    
    el.style.position = "absolute";
    el.style.top = 0;
    el.style.left = 0;
    el.style.width = w + "px";
    el.style.height = h + "px";
    el.style.border = 0;
    
    this.conf.element = el;
    panes.overlayLayer.appendChild(el);
    
    var overlay = this;
    
    // this somehow fakes responsiveness and has to be redesigned
    var DELAY = 1000;
    var delayTimer = null;
    google.maps.event.addListener(overlay.getMap(), 'idle', function() {
        if (overlay.skipDrawOnIdleOnce) {
            overlay.skipDrawOnIdleOnce = false;
            return;
        }
        delayTimer = setTimeout(function() {
            overlay.forceDraw();
            overlay.suppressDraw = true;
            delayTimer = null;
        }, DELAY);
    });
    google.maps.event.addListener(overlay.getMap(), 'center_changed', function() {
        overlay.heatmap.interrupt();
        overlay.heatmap.clear();
        if (delayTimer)
            clearTimeout(delayTimer);
    });
    
    this.heatmap = heatmapFactory.create(this.conf);
};

HeatmapOverlay.prototype.onRemove = function() {
    // Empty for now.
};

HeatmapOverlay.prototype.draw = function() {
    
    if (this.suppressDraw || this.isEmpty)
        return;
    
    var bounds = this.map.getBounds();
    
    // ne & sw on the huge overlay div
    var projection = this.getProjection();
    var ne = projection.fromLatLngToDivPixel(bounds.getNorthEast());
    var sw = projection.fromLatLngToDivPixel(bounds.getSouthWest());
    var topY = ne.y;
    var leftX = sw.x;
    var h = sw.y - ne.y;
    var w = ne.x - sw.x;
    var heatmap = this.heatmap;
    
    this.conf.element.style.left = leftX + 'px';
    this.conf.element.style.top = topY + 'px';
    this.conf.element.style.width = w + 'px';
    this.conf.element.style.height = h + 'px';
    heatmap.resize(heatmap.acanvas, heatmap.canvas);
    
    var self = this;
    this.taskCallback(function() {
        self.innerSetDataSet();
        if (heatmap.animated)
            heatmap.resume();
        else
            heatmap.drawDataSet();
    }, "Generating heatmap...");
};

HeatmapOverlay.prototype.forceDraw = function() {
    var suppressFlag = this.suppressDraw;
    this.suppressDraw = false;
    this.draw();
    this.suppressDraw = suppressFlag;
};

HeatmapOverlay.prototype.setDataSet = function(data) {
    var dlen = data.length;
    
    this.isEmpty = dlen == 0;
    var latLngPerPixel = this._computeLatLngPerPixel();
    var cityBounds = this.cityBounds;
    
    for ( var i = 0; i < dlen; i += 1) {
        var dataPoint = data[i];
        
        if (isNaN(dataPoint.lat) || isNaN(dataPoint.lng))
            continue;
        
        var latlng = new google.maps.LatLng(dataPoint.lat, dataPoint.lng);
        if (!cityBounds.contains(latlng))
            continue;
        
        this.rtree.insert({
            x: dataPoint.lng,
            y: dataPoint.lat,
            w: latLngPerPixel.lngPerPixel,
            h: latLngPerPixel.latPerPixel
        }, dataPoint);
    }
    
    this.innerSetDataSet();
};

HeatmapOverlay.prototype.innerSetDataSet = function() {
    var mapdata = {
        max: 1.0,
        data: []
    };
    var heatmap = this.heatmap;
    var bounds = this.map.getBounds();
    var ne = bounds.getNorthEast();
    var sw = bounds.getSouthWest();
    
    var visiblePoints = this.rtree.search({
        x: sw.lng(),
        y: sw.lat(),
        w: ne.lng() - sw.lng(),
        h: ne.lat() - sw.lat()
    });
    var dlen = visiblePoints.length;
    
    var projection = this.getProjection();
    
    visiblePoints.sort(function(a, b) {
        return a.createdAt - b.createdAt;
    });
    for ( var i = 0; i < dlen; i += 1) {
        var dataPoint = visiblePoints[i];
        
        var latlng = new google.maps.LatLng(dataPoint.lat, dataPoint.lng);
        var point = projection.fromLatLngToContainerPixel(latlng);
        
        mapdata.data.push({
            x: Math.floor(point.x),
            y: Math.floor(point.y),
            count: dataPoint.count,
            time: dataPoint.createdAt
        });
    }
    
    heatmap.clear();
    heatmap.store.setDataSet(mapdata);
};

HeatmapOverlay.prototype.addDataPoint = function(lat, lng, count) {
    var projection = this.getProjection();
    var latlng = new google.maps.LatLng(lat, lng);
    var point = projection.fromLatLngToContainerPixel(latlng);
    this.heatmap.store.addDataPoint(point.x, point.y, count);
};

HeatmapOverlay.prototype.toggle = function() {
    this.heatmap.toggleDisplay();
};

HeatmapOverlay.prototype.play = function() {
    this.heatmap.play();
};

HeatmapOverlay.prototype.pause = function() {
    this.heatmap.pause();
};

HeatmapOverlay.prototype.next = function() {
    this.heatmap.drawNextFrame();
};

HeatmapOverlay.prototype.previous = function() {
    this.heatmap.drawPreviousFrame();
};

HeatmapOverlay.prototype.getState = function() {
    if (!this.heatmap)
        return "pause";
    return this.heatmap.state;
};

HeatmapOverlay.prototype.toggleTimeWindow = function() {
    this.heatmap.toggleTimeWindow();
};

HeatmapOverlay.prototype.searchNearest = function(latLng, width) {
    log.info("searching tweets near ..." + JSON.stringify(latLng) + " with bbox width "
        + width);
    
    var latLngPerPixel = this._computeLatLngPerPixel();
    
    var half_width = Math.floor(width / 2) * latLngPerPixel.lngPerPixel;
    var result = this.rtree.search({
        x: latLng.lng() - half_width,
        y: latLng.lat() - half_width,
        w: width * latLngPerPixel.lngPerPixel,
        h: width * latLngPerPixel.latPerPixel
    });
    log.info("found " + result.length + " nearby points.");
    
    var idSet = [];
    
    var dlen = result.length;
    while (dlen--) {
        idSet.push(result[dlen].tweetId);
    }
    
    return idSet;
};

HeatmapOverlay.prototype._computeLatLngPerPixel = function() {
    var bounds = this.map.getBounds();
    var ne = bounds.getNorthEast();
    var sw = bounds.getSouthWest();
    var latDiff = ne.lat() - sw.lat();
    var lngDiff = ne.lng() - sw.lng();
    var mapDiv = this.map.getDiv();
    var divWidth = mapDiv.clientWidth;
    var divHeight = mapDiv.clientHeight;
    var latPerPixel = latDiff / divHeight;
    var lngPerPixel = lngDiff / divWidth;
    
    return {
        latPerPixel: latPerPixel,
        lngPerPixel: lngPerPixel
    };
};
