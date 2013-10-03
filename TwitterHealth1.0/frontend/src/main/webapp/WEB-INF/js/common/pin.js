
function TwitterHealthPin() {
	this.id = null;
    this.color = null;
	this.time = null;
	this.position = null;
	this.window = null;
	this.canvas = null;
	this.width = 0;
	this.height = 0;
	
	this.onAdd = function() {
	    var context = this;
	    
	    // click handler
	    google.maps.event.addDomListener(this.canvas, 'click', function() {
	        if(!!activeInfoWindow) activeInfoWindow.close();
    		context.window.open(context.getMap(), context);
    		activeInfoWindow = context.getWindow();
    		activePin = context;
	    });
	    
	    // display proper cursor
	    google.maps.event.addDomListener(this.canvas, 'mouseover', function() {
    		$(this).css('cursor', 'pointer');
    	});

    	google.maps.event.addDomListener(this.canvas, 'mouseout', function() {
    		$(this).css('cursor', 'default');
    	});
    	
    	// add dom elements to map panes
    	var panes = this.getPanes();
    	panes.overlayMouseTarget.appendChild(this.canvas);
	};
	
	this.onRemove = function() {
	    $(this.canvas).remove();
	};
	
	this.computeTime = function(t) {
	    var timestr = t.created_at.match(/^([A-Za-z]{3}), ([0-9]{2}) ([A-Za-z]{3}) ([0-9]{4}) ([0-9]{2}):([0-9]{2}):([0-9]{2})/g);
        var ti = timestr[0].split(/\s/g);
        ti[2] = monthMap[ti[2]];
        var d_datestr = ti[2] + ' ' + ti[1] + ', ' + ti[3] + ' ' + ti[4];
        var d_tweet_time = new Date(d_datestr);
        return d_tweet_time.getTime();
	};
    
    this.processTweet = function(t) {
        this.id = t._id;
        this.color = this.computeColor(t);
        this.time = this.computeTime(t);
        this.position = this.computePosition(t);
        this.window = new google.maps.InfoWindow({
            content: this.computeInfoWindow(t)
        });
        this.canvas = document.createElement('canvas');
        this.canvas.width = this.getWidth();
        this.canvas.height = this.getHeight();
        this.canvas.style.zIndex = 1000;
        this.canvas.style.position = 'absolute';
    };
    
    // getters and setters
    this.getId =       function() { return this.id; };
    this.getColor =    function() { return this.color; };
	this.getTime =     function() { return this.time; };
	this.getPosition = function() { return this.position; };
	this.getWindow =   function() { return this.window; };
	this.getCanvas =   function() { return this.canvas; };
	this.getWidth =    function() { return this.width; };
	this.getHeight =   function() { return this.height; }; 
}

function PollutionPin(tweet, city, map) {
    this.width = 12;
    this.height = 12;
    this.city = city;
    
    this.draw = function() {
        // set proper bounds
        var canvas = this.getCanvas();
    	var projection = this.getProjection();
    	var oldPos = projection.fromLatLngToDivPixel(this.getPosition());
    	var w = this.getWidth(), h = this.getHeight();
    	canvas.style.top = (oldPos.y - h/2) + 'px';
    	canvas.style.left = (oldPos.x - w/2) + 'px';
        
    	var imgAlpha = this.computeAlpha(4); // looks back four days
    	if(imgAlpha > 0.0 && imgAlpha <= 1.0)
    		canvas.style.visibility = "visible";
    	else {
    		canvas.style.visibility = "hidden";
    		return;
		}

    	// draw pin, set alpha
    	var pincontext = canvas.getContext('2d');
    	pincontext.clearRect(0, 0, w, h);
    	pincontext.globalAlpha = imgAlpha;
    	pincontext.beginPath();
        pincontext.arc(w/2, h/2, w/2 - 1, 0, 2*Math.PI, false);
        pincontext.fillStyle = this.getColor();
        pincontext.fill();
        pincontext.lineWidth = 1;
        pincontext.strokeStyle = "black";
        pincontext.stroke();
    };
    
    this.computeAlpha = function(lookback) {
        // get time difference ratio, calculate alpha
    	var value = parseInt($('#sliderVal_hold').html());
    	var daysMs = value * 2 * 60 * 60 * 1000;
    	var lookbackMs = lookback * 24 * 60 * 60 * 1000;
    	var todayMidnight = dateRanges[getCity()].last;
    	var otherDay = new Date(todayMidnight.getTime() + daysMs);
    	var diff = otherDay.getTime() - this.time;
    	
    	return 1 - (diff / lookbackMs);
    };
    
    this.computeColor = function(t) { return getColorForRating(t.health); };
    
    this.computePosition = function(t) {
        // TODO: Hacky! get rid of it
	    var lat = (api == "pollution" && this.city == 'nyc') ? t.lat : t.geo.coordinates[0];
        var lng = (api == "pollution" && this.city == 'nyc') ? t.lon : t.geo.coordinates[1];
        return new google.maps.LatLng(lat, lng);
	};
    
    this.computeInfoWindow = function(t) {
        return '<div class="container">\n' +
            '<div class="snippet">\n' +
                '<img class="photo" width="85px" height=85px" src="' + t.profile_image_url + '" alt="Profile Image" ' +
                    'onerror="this.src = \'/css/images/profile_pic_default.png\'" />\n' +
                '<a href="#" class="map-link" alt="show ' + t.from_user + ' on the map">\n' +
                    '<span class="fn org">' + t.from_user + '</span>\n' +
                    '<font style="color:red; font-size:large">' + t.health.toFixed(2) + '</font>\n' +
                '</a>\n' +
                '<div class="announcement">' + t.text + '</div>\n' +
                // temporarily disable timestamp
                /*'<div class="timeStamp">' + tweet.created_at + '</div>\n' +*/
            '</div>\n' +
        '</div>';
    };
    
    this.processTweet = function(t) {
        PollutionPin.prototype.processTweet.call(this, t);
        var day = new Date(this.time).toDateString();
        if($.inArray(day, daysWithTweets[city]) == -1)
            daysWithTweets[city].push(day);
    };
    
    this.getCity = function() { return this.city; };
    
    this.processTweet(tweet);
    this.setMap(map);
}

function DiseasesPin(tweet, map) {
    this.width = 4;
    this.height = 4;
    this.snippet = null;
    
    this.draw = function() {
        // set proper bounds
        var canvas = this.getCanvas();
    	var projection = this.getProjection();
        var oldPos = projection.fromLatLngToDivPixel(this.getPosition());
    	var w = this.getWidth(), h = this.getHeight();
        canvas.style.top = (oldPos.y - h/2) + 'px';
        canvas.style.left = (oldPos.x - w/2) + 'px';
        
        // draw pin
        var pincontext = canvas.getContext('2d');
    	pincontext.clearRect(0, 0, w, h);
    	pincontext.beginPath();
        pincontext.arc(w/2, h/2, w/2, 0, 2*Math.PI, false);
        pincontext.fillStyle = this.getColor();
        pincontext.fill();
    };
    
    this.computeColor = function(t) { return getColorByDisease(t.taxonomy.disease); };
    
    this.computePosition = function(t) {
	    var lat = t.geo.coordinates[0], lng = t.geo.coordinates[1];
        return new google.maps.LatLng(lat, lng);
	};
    
    this.computeInfoWindow = function(t) {
        var color = getColorByDisease(t.taxonomy.disease);
        var findterm = new RegExp(t.taxonomy.terms, "gi");
        var text_highlight = t.text.replace(findterm, '<span style="font-weight:900; color:'
            + color + '">' + t.taxonomy.terms + '</span>');
        var name_highlight = t.from_user.replace(findterm, '<span style="font-weight:900; color:'
            + color + '">' + t.taxonomy.terms + '</span>');
        return '<div class="container">\n' +
            '<div class="snippet" style="border: solid 1px ' + color + '">\n' +
                '<a href="#" class="map-link" alt="show ' + t.from_user + ' on the map">\n' +
                    '<font style="color:' + color + '; font-size:large">\n' + 
                        '<span class="fn org">' + name_highlight + '</span>\n' +
                        '[' + t.taxonomy.disease + ']\n' +
                    '</font>\n' +
                '</a>\n' +
                '<div class="announcement">' + text_highlight + '</div>\n' +
                '<div class="timeStamp">' + t.created_at + '</div>\n' +
            '</div>\n' +
        '</div>';
    };
    
    this.computeSnippet = function(t) {
        var color = getColorByDisease(t.taxonomy.disease);
        var findterm = new RegExp(t.taxonomy.terms, "gi");
        var text_highlight = t.text.replace(findterm,
            '<span style="font-weight:900; color:' + color + '">' + t.taxonomy.terms + '</span>');
        var name_highlight = t.from_user.replace(findterm,
            '<span style="font-weight:900; color:' + color + '">' + t.taxonomy.terms + '</span>');
        return '<div class="snippet" style="border-bottom: solid 1px #555555">\n' +
            '<a href="#" class="map-link" alt="show ' + t.from_user + ' on the map">\n' +
                '<font style="color:' + color + '">\n' + 
                    '<span class="fn org" style="font-size:14px">' + name_highlight + ':</span>\n' +
                '</font>\n' +
            '</a>\n' +
            text_highlight +
            '<font style="color:' + color + '"> [' + t.taxonomy.disease + ']</font>\n' +
            '<div class="timeStamp">' + t.created_at + '</div>\n' +
        '</div>';
    };
    
    this.getSnippet = function() { return this.snippet; };
    
    this.processTweet = function(t) {
        DiseasesPin.prototype.processTweet.call(this, t);
        this.snippet = this.computeSnippet(t);
    };

    this.processTweet(tweet);
    this.setMap(map);
}

TwitterHealthPin.prototype = new google.maps.OverlayView();
PollutionPin.prototype = new TwitterHealthPin();
DiseasesPin.prototype = new TwitterHealthPin();