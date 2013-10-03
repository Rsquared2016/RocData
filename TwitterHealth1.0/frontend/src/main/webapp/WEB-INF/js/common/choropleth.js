
function Choropleth(map) {
    this.mapSave = map;
    this.geoJson = null;
    this.dataLoaded = false;
    this.queuedDraw = false;
    this.layer = null;
    this.adminDivisions = null;
    this.selected = null;
    this.info = {};
    this.infoWindow = new google.maps.InfoWindow({ disableAutoPan: true });
    var self = this;
    
    // semaphore for queued draw commands
    $(document).bind("census-loaded", function() {
        if(self.queuedDraw)
            self.setMap(self.mapSave);
    });
    
    // summon census information from the forgotten galaxy of dementia five
    $.getJSON("/resources/data/census.json", function(data) {
        self.geoJson = data;
        $.each(data, function(index, zip) {
            self.info[zip.id] = zip.properties;
            self.info[zip.id].infoPoint = new google.maps.LatLng(
                zip.geometry.coordinates[0][0][1], zip.geometry.coordinates[0][0][0]);
        });
        $(document).trigger("census-loaded");
    });
};

Choropleth.prototype = new google.maps.OverlayView();

Choropleth.prototype.onAdd = function() {
    // queue draw if we're loading data
    if(!this.geoJson) {
        this.queuedDraw = true;
        return;
    }
    
    // initialize DOM elements for polygons
    this.layer = d3.select(this.getPanes().overlayMouseTarget)
        .append("div")
        .attr("class", "SvgOverlay");
    var svg = this.layer.append("svg");
    this.adminDivisions = svg.append("g").attr("class", "AdminDivisions");
};

Choropleth.prototype.draw = function() {
    var self = this;
    var overlayProjection = this.getProjection();
    
    // Turn the overlay projection into a d3 projection
    var googleMapProjection = function(coordinates) {
        var googleCoordinates = new google.maps.LatLng(coordinates[1], coordinates[0]);
        var pixelCoordinates = self.getProjection()
            .fromLatLngToDivPixel(googleCoordinates);
        return [pixelCoordinates.x + 4000, pixelCoordinates.y + 4000];
    };
    
    var d3Projection = function(position) {
        var d3Coordinates = new google.maps.Point(position[0], position[1]);
        return self.getProjection().fromDivPixelToLatLng(d3Coordinates);
    };

    var path = d3.geo.path().projection(googleMapProjection);
    this.adminDivisions.selectAll("path")
        .data(this.geoJson)
        .attr("d", path) // update existing paths
        .enter()
        .append("svg:path")
        .attr("id", function(d, i) { return d.id; })
        .attr("d", path)
        // show a zip code's census info
        .on("click", function() {
            if(this != self.selected) {
                d3.select(this).style("fill", "orange").style("stroke", "orange");
                var id = $(this).attr("id");
                if(self.selected) {
                    d3.select(self.selected)
                        .style("fill", "white")
                        .style("stroke", "white");
                    self.infoWindow.close();
                    self.infoWindow.setContent("");
                }
                self.selected = this;
                // TODO: when this page is require.js-ified, make this a template
                var content = "<h3>" + id + "</h3>"
                $.each(self.info[id], function(key, value) {
                    content += ("<div>" + key.replace(/\_/g, " ") + ": " + value + "</div>");
                });
                self.infoWindow.setContent(content);
                var coords = self.info[id].infoPoint;
                self.infoWindow.setPosition(coords);
                self.infoWindow.open(self.getMap());
            } else {
                d3.select(this).style("fill", "white").style("stroke", "white");
                self.infoWindow.close();
                self.infoWindow.setContent("");
                self.selected = null;
            }
        });
};

Choropleth.prototype.onRemove = function() {
    this.infoWindow.close();
    this.infoWindow.setContent("");
    this.selected = null;
    $(this.layer).remove();
};

Choropleth.prototype.show = function() {
    this.setMap(this.mapSave);
};

Choropleth.prototype.hide = function() {
    this.setMap(null);
};