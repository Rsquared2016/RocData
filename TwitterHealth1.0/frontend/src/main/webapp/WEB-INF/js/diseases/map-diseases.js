
var map = null;
var twitterHealthPins = {};
var twitterInfoWindows = {};
var activeInfoWindow = null;
var activePin = null;
var allControls = {};
var dataUrl = null;
var reload = true;
// days hardcoded in JSON for demos and such
var hardDays = ['2012-05-20', '2012-05-21', '2012-05-22', '2012-05-23',
    '2012-05-24', '2012-05-25', '2012-05-26'];
// semaphores for triggering snippets
var tweetsLoaded = false;
var countsLoaded = false;
//var pageLink = '${pageLink}';
//var pageMode = '${pageMode}';

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

var tableMap = {
    diseases: 'diseases'
};

var changePolls = {};
var allTweets = {};
var daysWithTweets = {
    diseases: []
}

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
        minZoom: 4,
        maxZoom: 16,
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
	
	map.fitBounds(getBoundsUS());
	
	// position/hide animation
	$("#loading_anim img").hide();
	
	google.maps.event.addListenerOnce(map, 'tilesloaded', function(event) {
        $("#loading_anim img").position({ my: "center center", at: "center center", of: "#loading_anim" });
        $("#loading_anim div").position({ my: "center center", at: "center center", of: "#loading_anim" });
	});

    // handler for bbox change
    google.maps.event.addListenerOnce(map, 'idle', function() {
        load("diseases", map.getBounds());
        google.maps.event.addListener(map, 'idle', function() {
            // put map bounds info
            var sw = map.getBounds().getSouthWest(), ne = map.getBounds().getNorthEast();
            var bounds1 = map.getBounds();
            window.setTimeout(function() {
                // reload for new bounding box
                if(bounds1 == map.getBounds()){
                    // don't reload if view was nudged by info window
                    if(activeInfoWindow == null || activePin == null ||
                        !bounds1.contains(activePin.getPosition())) {
                        // be sure to clear active pin and window
                        activeInfoWindow = null;
                        activePin = null;
                        // --- clear the old pins
                        if(!!allTweets) {
                            $.each(allTweets, function(i, tweet) {
                                tweet.setMap(null);
                            });
                        }
                        allTweets = {};
                        // --- Retrieve the new ones.
                        load("diseases", bounds1);
                    }
                }
            }, 1500);
        });
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
function load(name, bounds) {
    // show anim
    $("#loading_anim img").show();
    if($("#notweets").length > 0)
        $("#notweets").hide();
    //var dataUrl = "/resources/scripts/data/" + getDayPageName() + ".json";
    //var statsUrl = "/resources/scripts/stats/" + getDayPageName() + ".json";
    var dataUrl = getUrl(true, bounds);
    var statsUrl = getStatsUrl(true, bounds);
    var snip = {};
    // reset load semaphores
    tweetsLoaded = false;
    countsLoaded = false;
    
    // get tweets
    $.getJSON(dataUrl, function(data) {
        // display message for no tweets
        if(data.tweets.length <= 0) {
            $("#loading_anim img").hide();
            if($("#notweets").length <= 0)
                $("#loading_anim").append('<div id="notweets" style="width: 100%; color:white; text-align:center">No tweets to load for this day.</div>');
            else
                $("#notweets").show();
            return;
        }

        // iterate over this day
        $.each(data.tweets, function(i, tweet) {
            //addTweet(tweet, name, map, false);
            var pin = new DiseasesPin(tweet, map);
            allTweets[tweet._id] = pin;

            // add snippets
            var index = isDiseasePage() ? tweet.taxonomy.terms : tweet.taxonomy.disease.replace(/[^A-Za-z]/g, '');
            if(!snip[index]) snip[index] = [];

            if(snip[index].length < 4) {
                snip[index].push(pin.getSnippet());
                /*$("div#" + index).children("#" + snip[index]).empty();
                $("div#" + index).children("#" + snip[index]).append(snippet);*/
            }

            // turn off loading anim
            if(i == data.tweets.length - 1)
                $("#loading_anim img").hide();
        });
        
        // try to add snippets
        tweetsLoaded = true;
        $(document).trigger('addSnippets');
    });    

    // process stats
    $.getJSON(statsUrl, function(stats) {
        // reduce new dataset and draw new page bottom
        var dataCount = fullyReduce(stats.statistics.daily);
        dataCount.sort(function(a, b) { return b.value - a.value; });
        processCounts(dataCount);

        // reduce new dataset and draw fresh histograms
        dataHist = fullyReduce(stats.statistics.hourly);
        processHistograms(dataHist);
    });
    
    // handler for adding snippets when everything's ready
    $(document).bind('addSnippets', function(event) {
        if(tweetsLoaded && countsLoaded) {
            $.each(snip, function(disease, snippets) {
                $.each(snippets, function(i, snippet) {
                    $("div#" + disease).children("#" + i).empty();
                    $("div#" + disease).children("#" + i).append(snippet);
                });
            });
        }
    });
}

function loadStats(name, bounds) {
    // show anim
    $("#loading_anim img").show();
    var dataUrl = getStatsUrl(true, bounds);
    $.getJSON(dataUrl, function(data) {
        // sort new dataset and process count/histogram info
        var stats = data.statistics;
        stats.sort(function(a, b) { return b.value - a.value; });
        processCounts(stats);
        processHistograms(dataHist);
    });
}

// longpoll handlers: check for changes
// props to koleto of stackoverflow
function longpoll(name, since) {
    $.getJSON('/changes/' + name + '?since=' + since, function(changes) {
        // logging for sanity purposes
        log.info("Polling " + name + " API for changes...");
        log.info("Changes: ");
        // add changes
        $.each(changes.tweets, function(i, tweet) {
           allTweets[tweet._id] = new DiseasesPin(tweet, map);
        });
	    // restart poll timer
	    changePolls[name] = setTimeout(function() {
            longpoll(name, changes.updateSequence);
        }, 60000);
    });
}

function getUrl(isDataUrl, bounds, disease) {
    var url = isDataUrl ? "/data/diseases" : "/diseases";
    bounds = bounds != null ? bounds : getBoundsUS();
    var n = bounds.getNorthEast().lat(), e = bounds.getNorthEast().lng();
    var s = bounds.getSouthWest().lat(), w = bounds.getSouthWest().lng();
    // get page vars from jsp
    var day = getDayPageName(), hour = getHourPageName();
    var dis = getDiseasePageName(), tag = getTagPageName();
    url += (isDataUrl ? ("/" + s + "/" + w + "/" + n + "/" + e) : "");
    url += (day != "" ? "/" + day : "/" + getDateString(new Date().toDateString()));
    url += (hour != "" ? "/" + hour : (!!disease ? "/all" : ""));
    url += (!!disease ? "/" + disease : (dis != "" ? "/" + dis : ""));
    url += (tag != "" ? "/" + tag : "");
    
    return url;
}

function getStatsUrl(isDataUrl, bounds, disease) {
    var url = isDataUrl ? "/data/stats" : "/diseases";
    bounds = bounds != null ? bounds : getBoundsUS();
    var n = bounds.getNorthEast().lat(), e = bounds.getNorthEast().lng();
    var s = bounds.getSouthWest().lat(), w = bounds.getSouthWest().lng();
    // get page vars from jsp
    var day = getDayPageName(), hour = getHourPageName();
    var dis = getDiseasePageName(), tag = getTagPageName();
    url += (isDataUrl ? ("/" + s + "/" + w + "/" + n + "/" + e) : "");
    url += (day != "" ? "/" + day : "/" + getDateString(new Date().toDateString()));
    url += (hour != "" ? "/" + hour : (!!disease ? "/all" : ""));
    url += (!!disease ? "/" + disease : (dis != "" ? "/" + dis : ""));
    url += (tag != "" ? "/" + tag : "");
    
    return url;
}

function getDateString(day) {
    var d = new Date(day);
    var mo = d.getMonth() < 9 ? "0" + (d.getMonth() + 1) : "" + (d.getMonth() + 1);
    var date = d.getDate() < 10 ? "0" + d.getDate() : "" + d.getDate();
    var dayUnderscores = d.getFullYear() + "-" + mo + "-" + date;
    return dayUnderscores;
}