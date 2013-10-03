CombinedLayersOverlay.prototype = new google.maps.OverlayView();

function CombinedLayersOverlay(map, options) {
    this.setMap(map);
    this.markers = {};
    this.options = options;
}

CombinedLayersOverlay.prototype.onAdd = function() {
    var panes = this.getPanes(), canvasDiv = document.createElement("div");

    canvasDiv.style.position = "absolute";
    canvasDiv.style.left = 0 + 'px';
    canvasDiv.style.top = 0 + 'px';
    this.canvasDiv = canvasDiv;

    panes.overlayLayer.appendChild(canvasDiv);
    var canvas = document.createElement("canvas");
    this.canvas = canvas;
    canvasDiv.appendChild(canvas);
    this.ctx = canvas.getContext("2d");

    var overlay = this;
    google.maps.event.addListener(overlay.getMap(), 'center_changed',
            function() {
                overlay.draw();
            });
};

CombinedLayersOverlay.prototype.onResize = function() {
    // just resize the canvas
    var canvas = this.canvasDiv;
    var projection = this.getProjection();
    var bounds = this.getMap().getBounds();
    var sw = projection.fromLatLngToDivPixel(bounds.getSouthWest());
    var ne = projection.fromLatLngToDivPixel(bounds.getNorthEast());
    var topY = ne.y, leftX = sw.x, h = sw.y - ne.y, w = ne.x - sw.x;
    var ctx = this.ctx;

    canvas.style.left = leftX + 'px';
    canvas.style.top = topY + 'px';
    ctx.canvas.height = h;
    ctx.canvas.width = w;
    log.info("CombinedLayersOverlay's canvas resized, new dimension: [" + w
            + ", " + h + "]");
};

CombinedLayersOverlay.prototype.draw = function() {
    this.onResize();
};

CombinedLayersOverlay.prototype.drawLayers = function(options, layers) {
    log.info("drawing layers...");

    var ctx = this.ctx;
    var projection = this.getProjection();
    var bounds = this.getMap().getBounds();
    var sw = projection.fromLatLngToDivPixel(bounds.getSouthWest());
    var ne = projection.fromLatLngToDivPixel(bounds.getNorthEast());
    var h = sw.y - ne.y, w = ne.x - sw.x;
    var globalAlpha = this.options.globalAlpha;

    switch (options.mode) {
    case "graphical":
        log.info("using graphical mode");
        ctx.clearRect(0, 0, w, h);
        ctx.globalAlpha = globalAlpha;

        var layer;
        for ( var int = 0; int < layers.length; int++) {
            layer = layers[int];
            layer.draw({
                canvasCtx : this.ctx,
                map : this.getMap(),
                projection : this.getProjection()
            });
        }
        break;
    case "numerical":
        // to be implemented
        break;
    }
};
