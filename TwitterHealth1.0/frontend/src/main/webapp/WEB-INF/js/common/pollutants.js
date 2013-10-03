function getPollutantTypeMarker(oldMarker) {
    if (oldMarker == null)
        return null;
    var newUrl = 'http://labs.google.com/ridefinder/images/mm_20_purple.png';
    return new google.maps.MarkerImage(newUrl, oldMarker.size, oldMarker.origin,
        oldMarker.anchor);
}

function PollutantTrackerHeatmap(file, map, parser) {
    // initialize
    this.map = map;
    this.file = file;
    this.active = false;
    this.data = [];
    var self = this;
    this.markers = [];
    this.lastMarker = null;
    var psw = new google.maps.LatLng(40.467597, -74.409908);
    var pne = new google.maps.LatLng(41.046156, -73.548989);
    var nybounds = new google.maps.LatLngBounds(psw, pne);
    self.heatmap = new HeatmapOverlay(this.map, {
        radius: 15,
        visible: false,
        opacity: 60,
        // gradient is shades of violet (near: darker, far: lighter)
        gradient: {
            "0.40": "rgb(204,71,204)",
            "0.55": "rgb(179,62,179)",
            "0.70": "rgb(153,53,153)",
            "0.85": "rgb(128,45,128)",
            "1.00": "rgb(102,36,102)"
        },
        animated: false,
        initialState: "none",
        cityBounds: nybounds,
        taskCallback: function(task, text) {
            setTimeout(function() {
                task();
            }, 15);
        }
    });
    this.kmlParser = new geoXML3.parser({
        map: this.map,
        zoom: false,
        createMarker: function(placemark, doc) {
            self.data.push({
                lat: placemark.point.lat,
                lng: placemark.point.lng,
                count: 0.70,
                createdAt: 0
            });
            
            return null;
        },
        afterParse: function() {
            // nothing
        }
    });
    this.kmlParser.parse(this.file);
}

PollutantTrackerHeatmap.prototype.show = function() {
    if (this.heatmap.isEmpty)
        this.heatmap.setDataSet(this.data);
    this.heatmap.toggle();
    this.heatmap.forceDraw();
    this.active = true;
};

PollutantTrackerHeatmap.prototype.hide = function() {
    this.heatmap.toggle();
    this.active = false;
};

function getPollutantTypeMarker(oldMarker) {
    if (oldMarker == null)
        return null;
    var newUrl = 'http://labs.google.com/ridefinder/images/mm_20_purple.png';
    return new google.maps.MarkerImage(newUrl, oldMarker.size, oldMarker.origin,
        oldMarker.anchor);
};

function PollutantTrackerPin(file, map) {
    // initialize
    this.map = map;
    this.file = file;
    this.active = false;
    this.markers = [];
    this.lastMarker = null;
    var cTracker = this;
    this.kmlParser = new geoXML3.parser({
        map: this.map,
        zoom: false,
        createMarker: function(placemark, doc) {
            var betterIcon = getPollutantTypeMarker(placemark.style.icon);
            var marker = new google.maps.Marker(
                {
                    map: map,
                    position: new google.maps.LatLng(placemark.point.lat,
                        placemark.point.lng),
                    title: placemark.name,
                    zIndex: Math.round(placemark.point.lat * 100000),
                    icon: betterIcon
                });
            marker.setVisible(false);
            
            // create reduced info window content
            var infoContent = document.createElement('div');
            $(infoContent).attr('id', 'infowindow');
            // add name and address, remove extraneous spacing
            $(infoContent).append('<h3>' + placemark.name + '</h3>');
            $(infoContent).children('h3').children('br').first().remove();
            // reduce size of address
            var headText = $(infoContent).text();
            var locName = headText.split(/:\s/)[0]
            var locAddr = headText.split(/:\s/)[1];
            $(infoContent).children('h3').text(locName);
            $(infoContent).append('<p>Address: ' + locAddr + '</p>');
            // add description, remove chart and "placeholder"
            if (placemark.description != null && placemark.description != "") {
                // console.log(placemark.description);
                // console.log(placemark.description.match(/<p>(.|\n)*<\/p>/g)[0]);
                var desc = placemark.description;
                // console.log(desc.match(/<p>(.|\n)*<\/p>/));
                var descontent = desc.match(/<p>(.|\n)*<\/p>/g)[0];
                $(infoContent).append('<div>' + descontent + '</div>');
            }
            /*
             * var descr =
             * $(infoContent).children('div').children('p').detach();
             * $(infoContent).children('div').remove();
             * $(infoContent).append(descr);
             */
            marker.infoWindow = new google.maps.InfoWindow({
                content: infoContent,
                pixelOffset: new google.maps.Size(0, 2)
            });
            
            google.maps.event.addListener(marker, 'click', function() {
                if (!!cTracker.lastMarker) {
                    cTracker.lastMarker.infoWindow.close();
                }
                marker.infoWindow.open(map, marker);
                cTracker.lastMarker = marker;
            });
            
            cTracker.markers.push(marker);
            return marker;
        }
    });
    this.kmlParser.parse(this.file);
}

PollutantTrackerPin.prototype.show = function() {
    $.each(this.markers, function(index, marker) {
        marker.setVisible(true);
    });
    this.active = true;
};

PollutantTrackerPin.prototype.hide = function() {
    $.each(this.markers, function(index, marker) {
        marker.setVisible(false);
    });
    if (!!this.lastMarker) {
        this.lastMarker.infoWindow.close();
        this.lastMarker = null;
    }
    this.active = false;
};

// --- Census Tracker
function CensusTracker(map) {
    // initialize
    this.map = map;
    this.active = false;
    this.choropleth = new Choropleth(map);
}

CensusTracker.prototype.show = function() {
    this.choropleth.show();
};

CensusTracker.prototype.hide = function() {
    this.choropleth.hide();
};

PollutantTrackerHeatmap.prototype.isActive = PollutantTrackerPin.prototype.isActive = CensusTracker.prototype.isActive = function() {
    return this.active;
};

function PollutantControls(map) {
    // initialize component divs and buttons
    this.map = map;
    this.activeButton = null;
    this.pollutantTrackers = {
        'Pollution Heatmap': new PollutantTrackerHeatmap(
            "/resources/kml/Top8NOxFacilitiesFiltered.kml", map),
        'Pollution Sites': new PollutantTrackerPin(
            "/resources/kml/Top8NOxFacilitiesFiltered.kml", map),
        'Census': new CensusTracker(map)
    };
    this.pollutantButtons = {};
    this.buttonsContainer = document.createElement('div');
    var self = this;
    $.each(self.pollutantTrackers, function(name, tracker) {
        self.pollutantButtons[name] = document.createElement('div');
        $(self.buttonsContainer).append(self.pollutantButtons[name]);
        $(self.pollutantButtons[name]).text(name);
    });
    // style
    this.buttonsContainer.style.height = '32px';
    this.buttonsContainer.style.padding = '10px';
    $(this.buttonsContainer).children().css({
        'width': '98px',
        'textAlign': 'center',
        'margin-left': '2px',
        'margin-right': '2px',
        'float': 'left'
    });
    $(this.buttonsContainer).children().addClass('ui-selectee');
    
    // event handlers
    $.each(self.pollutantButtons, function(index, button) {
        $(button).bind('click', function(event) {
            // get name
            var bName = $(event.currentTarget).text();
            
            // toggle active
            if (event.currentTarget != self.activeButton) {
                // show
                self.pollutantTrackers[bName].show();
                $(event.currentTarget).addClass('ui-selected');
                
                // hide formerly active button
                //if (!!self.activeButton) {
                    //var aName = $(self.activeButton).text();
                    //self.pollutantTrackers[aName].hide();
                    //$(self.activeButton).removeClass('ui-selected');
                //}
                
                self.activeButton = event.currentTarget;
            } else {
                // hide
                self.pollutantTrackers[bName].hide();
                $(event.currentTarget).removeClass('ui-selected');
                self.activeButton = null;
            }
        });
    });
    
    // not sure if this is really necessary
    this.buttonsContainer.index = 1;
    allControls['pollutantButtons'] = this;
}
