var map = null;
var twitterHealthPins = {};
var twitterInfoWindows = {};
var activeInfoWindow = null;
var changePolls = {};
var allTweets = {};
var allControls = {};
var dataUrl = null;
var choroplethOverlay = null;

var monthMap = {
	'Jan': 'January',
	'Feb': 'February',
	'Mar': 'March',
	'Apr': 'April',
	'May': 'May',
	'Jun': 'June',
	'Jul': 'July',
	'Aug': 'August',
	'Sep': 'September',
	'Oct': 'October',
	'Nov': 'November',
	'Dec': 'December'
};

var daysWithTweets = {
    nyc: [],
    boston: []
};

var dateRanges = (function() {
    var todayMidnight = new Date();
    todayMidnight.setHours(23, 59, 59, 999);
    var nyc = { first: new Date(2012, 6, 28, 23, 59, 59), last: todayMidnight };
    var nycOld = { first: new Date(2010, 4, 19, 23, 59, 59),
            last: new Date(2010, 5, 19, 23, 59, 59) };
    var boston = { first: new Date(2012, 6, 29, 23, 59, 59), last: todayMidnight };
    
    return { nyc: api == "pollution" ? nycOld : nyc, boston: boston };
})();

$(document).ready(function() {
	// create map
	map = new google.maps.Map(document.getElementById("map_canvas"), {
		center: new google.maps.LatLng(0.0, 0.0),
		mapTypeId: google.maps.MapTypeId.ROADMAP,
		zoom: 1,
        scrollwheel : true,
        draggable : true,
        navigationControl : false,
        mapTypeControl : false,
        scaleControl : false,
        disableDoubleClickZoom : false,
		styles:  [ 
					{
		    stylers: [
		      { invert_lightness: true },
		      { saturation: -56 },
		      { lightness: -56 },
		      { visibility: "simplified" }
		    ]
		  },{
		    featureType: "road",
		    stylers: [
		      { visibility: "simplified" },
		      { lightness: -34 },
		      { saturation: -44 },
		      { hue: "#00f6ff" }
		    ]
		  },{
		    featureType: "road",
		    elementType: "labels",
		    stylers: [
		      { visibility: "off" }
		    ]
		  },{
		    featureType: "water",
		    stylers: [
		      { hue: "#0066ff" },
		      { invert_lightness: true },
		      { saturation: -68 },
		      { lightness: -71 }
		    ]
		  }
 		],
 		zoomControlOptions: {
			style: google.maps.ZoomControlStyle.SMALL
		},
		draggableCursor: 'default'
	});
	
	// fit map to proper bounds
	var bounds = getBounds(defaultCity);
	map.fitBounds(bounds);
	
	// add controls
	google.maps.event.addListenerOnce(map, 'tilesloaded', function(event) {
		// create controls
		var timeDisplay = new TimeDisplay();
		var loadDisplay = new PinsLoadingDisplay();
        var citySelect = new CitySelector(map);
		var pinSlider = new PinSliderControl(timeDisplay);
		var timeControls = new TimeControls(pinSlider, timeDisplay);
		var pollutantButtons = new PollutantControls(map);
		var tutorialButton = new TutorialButton(map);
		var aboutButton = new AboutButton(map);
		var swapButton = new SwapPagesButton(map);
		// create traffic overlay controls
		var trafficControlUI = document.createElement('div');
		trafficControlUI.style.width = '98px';
		trafficControlUI.style.height = '18px';
		trafficControlUI.style.marginLeft = '12px';
		trafficControlUI.style.marginRight = '12px';
		trafficControlUI.style.marginBottom = '10px';
		trafficControlUI.style.textAlign = 'center';
		$(trafficControlUI).addClass('ui-selectee');
		$(trafficControlUI).text('Traffic');
		allControls['trafficControl'] = trafficControlUI;
		
		var trafficLayer = new google.maps.TrafficLayer();
        google.maps.event.addDomListener(trafficControlUI, 'click', function() {
            if (typeof trafficLayer.getMap() == 'undefined' || trafficLayer.getMap() === null) {
                $(trafficControlUI).addClass('gmap-control-active');
                trafficLayer.setMap(map);
            } else {
                trafficLayer.setMap(null);
                $(trafficControlUI).removeClass('gmap-control-active');
            }
        });
		          
		var legend = '<ul>'
		           + '<li><span style="background-color: #30ac3e">&nbsp;&nbsp;</span><span style="color: #30ac3e"> &gt; 80 km per hour</span></li>'
		           + '<li><span style="background-color: #ffcf00">&nbsp;&nbsp;</span><span style="color: #ffcf00"> 40 - 80 km per hour</span></li>'
		           + '<li><span style="background-color: #ff0000">&nbsp;&nbsp;</span><span style="color: #ff0000"> &lt; 40 km per hour</span></li>'
		           + '<li><span style="background-color: #c0c0c0">&nbsp;&nbsp;</span><span style="color: #c0c0c0"> No data available</span></li>'
		           + '</ul>';
		
		var trafficControlLegend = document.createElement('div');
		$(trafficControlLegend).addClass('gmap-control-legend');
		$(trafficControlLegend).html(legend);
		$(trafficControlLegend).hide();
		$(trafficControlUI).append(trafficControlLegend);
		
		// Set hover toggle event
		$(trafficControlUI).mouseenter(function() {
	        $(trafficControlLegend).show();
	    }).mouseleave(function() {
	        $(trafficControlLegend).hide();
	    });
		// add controls
		map.controls[google.maps.ControlPosition.TOP_RIGHT].push(pinSlider.sliderContainer);
		map.controls[google.maps.ControlPosition.RIGHT_TOP].push(timeControls.timeControlsContainer);
		map.controls[google.maps.ControlPosition.RIGHT_TOP].push(timeDisplay.timeOverlay);
		map.controls[google.maps.ControlPosition.LEFT_BOTTOM].push(pollutantButtons.buttonsContainer);
        map.controls[google.maps.ControlPosition.LEFT_BOTTOM].push(trafficControlUI);
		//map.controls[google.maps.ControlPosition.LEFT_BOTTOM].push(tutorialButton.buttonDiv);
		//map.controls[google.maps.ControlPosition.LEFT_BOTTOM].push(aboutButton.button);
		map.controls[google.maps.ControlPosition.BOTTOM_CENTER].push(loadDisplay.loadOverlay);
		//map.controls[google.maps.ControlPosition.LEFT_TOP].push(aboutButton.window.window);
		map.controls[google.maps.ControlPosition.RIGHT_BOTTOM].push(swapButton.button);
		map.controls[google.maps.ControlPosition.TOP_CENTER].push(citySelect.container);
		
		// retrieve initial tweets and draw markers
        var name = getCity();
        progressiveLoad(name);
		
		// stop loading animation
        $(loadDisplay.loadOverlay).trigger('stopLoadAnimation');
        // add hover stuff
        addHoverEvents();
	});
	
});

function getColorForRating(rating) {
	if(rating < .82){
		return "#BBFF33";
	}else if(rating < .84){
		return "#ccFF66";
	}else if(rating < .86){
		return "#DDFF99";
	}else if(rating < .88){
		return "#EEFFCC";
	}else if(rating < .90){
		return "#FFFFCC";
	}else if(rating < .92){
		return "#FFFF99";
	}else if(rating < .94){
		return "#FFFF66";
	}else if(rating < .96){
		return "#FFFF33";
	}else if(rating < .98){
		return "#FFFF00";
	}else if(rating < 1){
		return "#FFEECC";
	}else if(rating < 1.02){
		return "#FFDD99";
	}else if(rating < 1.04){
		return "#FFCC66";
	}else if(rating < 1.06){
		return "#FFBB33";
	}else if(rating < 1.08){
		return "#FFAA00";
	}else if(rating < 1.1){
		return "#FF7733";
	}else if(rating < 1.12){
		return "#D94426";
	}else if(rating < 1.14){
		return "#E63b19";
	}else if(rating < 1.16){
		return "#f2330d";
	}else{
		return "#ff0000";
	}
}

// loads tweets by day for a more responsive site appearance
function progressiveLoad(name) {
    // each day in time frame
    var days = getFullDateRange(name);
    $.each(days, function(index, day) {
        $.getJSON('/' + api + '/data/' + name + '?day=' + day, function(data) {
            // iterate over this day
            $.each(data.tweets, function(i, tweet) {
                allTweets[name] = allTweets[name] || {};
                allTweets[name][tweet._id] = new PollutionPin(tweet, name, map);
            });
            // add polling handlers first time around
            /*if(index == 0) {
                changePolls[name] = setTimeout(function() {
                    longpoll(name, data.updateSequence);
                }, 60000);
            }*/
        });
    });
}

// longpoll handlers: check for changes
// props to koleto of stackoverflow
function longpoll(name, since) {
    $.getJSON('/' + api + '/changes/' + name + '?since=' + since, function(changes) {
        // logging for sanity purposes
        log.info("Polling " + name + " API for changes...");
        log.info("Changes: ");
        // add changes
        $.each(changes.tweets, function(i, tweet) {
            log.info("" + i);
            allTweets[name] = allTweets[name] || {};
            allTweets[name][tweet._id] = new PollutionPin(tweet, name, map);
        });
	    // restart poll timer
	    changePolls[name] = setTimeout(function() {
            longpoll(name, changes.updateSequence);
        }, 60000);
    });
}

function getFullDateRange(name) {
    var range = [], dayMs = 86400000;
    var first = dateRanges[name].first.getTime();
    var last = dateRanges[name].last.getTime();
    for(var i = first; i <= last; i += dayMs) {
        var day = new Date(i);
        var mo = day.getMonth() < 9 ? "0" + (day.getMonth() + 1) : "" + (day.getMonth() + 1);
        var date = day.getDate() < 10 ? "0" + day.getDate() : "" + day.getDate();
        var dayIso = day.getFullYear() + "-" + mo + "-" + date;
        range.push(dayIso);
    }
    return range;
}

function addHoverEvents() {
	// handlers
	hin = function(event) { $(this).css('cursor', 'pointer'); };
	hout = function(event) { $(this).css('cursor', 'default'); };
	
	// add to individual controls
	$(allControls['aboutButton'].button).hover(hin, hout);
	$(allControls['aboutButton'].window.closeButton).hover(hin, hout);
	$(allControls['tutorialButton'].buttonDiv).hover(hin, hout);
	$(allControls['trafficControl']).hover(hin, hout);
	$.each(allControls.pollutantButtons, function(name, button) {
	    $(button).hover(hin, hout);
	});
	$(allControls['swapButton'].button).hover(hin, hout);
	$(allControls['timeControls'].timeControlsContainer).children().hover(hin, hout);
}
