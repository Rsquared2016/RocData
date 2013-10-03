
function TwitterHealthPin(tweet, city, map) {
	this.tweet_ = tweet.id;
	this.color_ = tweet.color;
	this.time_ = tweet.time;
	this.hold = null;
	this.canvas_ = document.createElement('canvas');
	this.canvas_.width = 4;
	this.canvas_.height = 4;
	this.canvas_.style.position = 'absolute';
	this.position_ = tweet.position;
	this.bounds_ = null;
	this.highlight = false;
	this.city = city;
	this.theMap = map;
	
	this.setMap(map);
}

TwitterHealthPin.prototype = new google.maps.OverlayView();

TwitterHealthPin.prototype.onAdd = function() {
	// bail if this is outside NYC or DC
	/*if(!inProperBounds(this)) {
		this.setMap(null);
		return;
	}*/
    
	// make sure info window appears
	var cmarker = this;
	google.maps.event.addDomListener(this.canvas_, 'click', function() {
		if(!!activeInfoWindow) {
			activeInfoWindow.close();
		}
		allTweets[cmarker.city][cmarker.tweet_].window.open(cmarker.getMap(), cmarker);
		activeInfoWindow = allTweets[cmarker.city][cmarker.tweet_].window;
		activePin = cmarker;
	});

	google.maps.event.addDomListener(this.canvas_, 'mouseover', function() {
		$(this).css('cursor', 'pointer');
	});

	google.maps.event.addDomListener(this.canvas_, 'mouseout', function() {
		$(this).css('cursor', 'default');
	});

	// add it to the overlays
	var panes = this.getPanes();
	panes.overlayMouseTarget.appendChild(this.canvas_);
}

TwitterHealthPin.prototype.onRemove = function() {
	$(this.canvas_).detach();
}

TwitterHealthPin.prototype.draw = function() {
	// don't draw if this pin was removed
	if(this.getMap() == null) return;

	// draw pin, set alpha
	var pincontext = this.canvas_.getContext('2d');
	var w = this.canvas_.width, h = this.canvas_.height;
	pincontext.clearRect(0, 0, w, h);
    //pincontext.drawImage(this.image_, 0, 0);
	pincontext.beginPath();
    pincontext.arc(w/2, h/2, w/2, 0, 2*Math.PI, false);
    pincontext.fillStyle = this.color_;
    pincontext.fill();

	// set proper bounds
	var projection = this.getProjection();
    var oldPos = projection.fromLatLngToDivPixel(this.position_);
    var swPoint = new google.maps.Point(oldPos.x - w/2, oldPos.y + h/2);
    var nePoint = new google.maps.Point(oldPos.x + w/2, oldPos.y - h/2);
    var swBound = projection.fromDivPixelToLatLng(swPoint);
    var neBound = projection.fromDivPixelToLatLng(nePoint);
    this.bounds_ = new google.maps.LatLngBounds(swBound, neBound);
    this.canvas_.style.top = (oldPos.y - h/2) + 'px';
    this.canvas_.style.left = (oldPos.x - w/2) + 'px';
    this.canvas_.style.width = '4px';
    this.canvas_.style.height = '4px';
	
	// pulse animation
	/*if(this.highlight && this.canvas_.style.visibility == "visible") {
	    $(this.canvas_).effect('pulsate', {times: 3}, 500);
	    this.highlight = false;
	}*/

	// re-render image
	/*$(this.image_).children('img').last().attr('src', this.canvas_.toDataURL());*/
}

TwitterHealthPin.prototype.getPosition = function() {
	return this.position_;
}

function PinsLoadingDisplay() {
	// create and style div
	this.loadOverlay = document.createElement('div');
	$(this.loadOverlay).attr('id', 'loadOverlay');
	// style
	this.loadOverlay.style.width = '400px';
	this.loadOverlay.style.paddingRight = '10px';
	this.loadOverlay.style.fontSize = '15px';
	this.loadOverlay.style.textAlign = 'center';
	this.loadOverlay.style.color = '#FFFFFF';
	this.loadOverlay.style.paddingBottom = '20px';
	$(this.loadOverlay).text('Loading Markers for Tweets...');
	$(this.loadOverlay).effect('pulsate', {}, 500);
	
	// event handler
	$(this.loadOverlay).bind('stopLoadAnimation', function() {
		var overlay = this;
		$(overlay).effect('fade', {}, 3000, function() {
			$(overlay).detach();
		});
	});
	
	// not sure if this is necessary
	this.loadOverlay.index = 1;
}

function addTweet(tweet, city, map, reload) {
    // create object for city
    if(!allTweets[city])
        allTweets[city] = {};

    // get tweet info
    var id = tweet._id;
    if(!allTweets[city][id] && !reload) {
        allTweets[city][id] = {};
        // TODO: make this geo in certain cases
        /*console.log(city + ' [' + id + ']: ');
        console.log('\t' + tweet.geo.coordinates[0] + ', ' + tweet.geo.coordinates[1]);*/
        var lat = city == 'nyc' ? tweet.lat : tweet.geo.coordinates[0];
        var lng = city == 'nyc' ? tweet.lon : tweet.geo.coordinates[1];
        var coords = new google.maps.LatLng(lat, lng);
        var color = getColorByDisease(tweet.taxonomy.disease);
        var ttime = tweet.created_at;

        // process time info
        var timestr = ttime.match(/^([A-Za-z]{3}), ([0-9]{2}) ([A-Za-z]{3}) ([0-9]{4}) ([0-9]{2}):([0-9]{2}):([0-9]{2})/g);
        var ti = timestr[0].split(/\s/g);
        ti[2] = monthMap[ti[2]];
        var d_datestr = ti[2] + ' ' + ti[1] + ', ' + ti[3] + ' ' + ti[4];
        var d_tweet_time = new Date(d_datestr);
        var d_tweet_ms = d_tweet_time.getTime();
        var day = d_tweet_time.toDateString();
        if($.inArray(day, daysWithTweets[city]) == -1)
        daysWithTweets[city].push(day);

        // make info window
        allTweets[city][id].window = new google.maps.InfoWindow({
            content: makeInfoWindow(tweet)
        });

        google.maps.event.addListener(allTweets[city][id].window, 'closeclick', function() {
            activeInfoWindow = null;
            activePin = null;
        });

        // make new marker
        allTweets[city][id].pin = new TwitterHealthPin({
            id: id,
            color: color,
            time: d_tweet_ms,
            position: coords
        }, city, map);
    }
}

function makeInfoWindow(tweet) {
    var color = getColorByDisease(tweet.taxonomy.disease);
    var findterm = new RegExp(tweet.taxonomy.terms, "gi");
    var text_highlight = tweet.text.replace(findterm,
        '<span style="font-weight:900; color:' + color + '">' + tweet.taxonomy.terms + '</span>');
    var name_highlight = tweet.from_user.replace(findterm,
        '<span style="font-weight:900; color:' + color + '">' + tweet.taxonomy.terms + '</span>');
    return '<div class="container">\n' +
                '<div class="snippet" style="border: solid 1px ' + color + '">\n' +
                    '<a href="#" class="map-link" alt="show ' + tweet.from_user + ' on the map">\n' +
                        '<font style="color:' + color + '; font-size:large">\n' + 
                            '<span class="fn org">' + name_highlight + '</span>\n' +
                            '[' + tweet.taxonomy.disease + ']\n' +
                        '</font>\n' +
                    '</a>\n' +
                    '<div class="announcement">' + text_highlight + '</div>\n' +
                    '<div class="timeStamp">' + tweet.created_at + '</div>\n' +
                '</div>\n' +
            '</div>';
}

function makeSnippet(tweet) {
    var color = getColorByDisease(tweet.taxonomy.disease);
    var findterm = new RegExp(tweet.taxonomy.terms, "gi");
    var text_highlight = tweet.text.replace(findterm,
        '<span style="font-weight:900; color:' + color + '">' + tweet.taxonomy.terms + '</span>');
    var name_highlight = tweet.from_user.replace(findterm,
        '<span style="font-weight:900; color:' + color + '">' + tweet.taxonomy.terms + '</span>');
    return '<div class="snippet" style="border-bottom: solid 1px #555555">\n' +
                '<a href="#" class="map-link" alt="show ' + tweet.from_user + ' on the map">\n' +
                    '<font style="color:' + color + '">\n' + 
                        '<span class="fn org" style="font-size:14px">' + name_highlight + ':</span>\n' +
                    '</font>\n' +
                '</a>\n' +
                text_highlight +
                '<font style="color:' + color + '"> [' + tweet.taxonomy.disease + ']</font>\n' +
                '<div class="timeStamp">' + tweet.created_at + '</div>\n' +
            '</div>';
}