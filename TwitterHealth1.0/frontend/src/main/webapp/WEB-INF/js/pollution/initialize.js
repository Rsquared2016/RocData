
// for everything you want to set after jMapping is done
// I put this in its own file so it's easier to manipulate
function onLoad_map(map, event) {
    var bounds = getBounds(getCity());
    map.fitBounds(bounds);
	
	// quick hack: zoom out boston a bit
	// TODO: get rid of this cause it's hacky...
	if(getCity() == 'boston') map.setZoom(map.getZoom() - 1);
}

function getCity() {
    try{return $(allControls['citySelect'].citySelect).children('option:selected').val();}
    catch(err){return 'US';}
}

function getLatLngBounds(bottomLeftLat, bottomLeftLong, topRightLat, topRightLong){
	return new google.maps.LatLngBounds(
			new google.maps.LatLng(bottomLeftLat, bottomLeftLong),
			new google.maps.LatLng(topRightLat, topRightLong)
	);
}
function getBoundsUS() {
    /* 28 parallels, 58 meridians */
	return getLatLngBounds(22.000,-123.000,50.000,-65.000);
}

function getBoundsNyc() {
	return getLatLngBounds(40.467597, -74.409908,41.046156, -73.548989);
}

function getBoundsDc() {
	return getLatLngBounds(38.793611, -77.271389, 38.987222, -76.815278);
}

function getBoundsLondon() {
    // N: 52.5032538, S: 50.5247462, E: 0.867253767, W: -1.11125377 
    return new getLatLngBounds(50.5247462, -1.11125377,52.5032538, 0.867253767);
}

function getBoundsCapetown() {
    // N: -32.968, S: -34.968, E: 19.577, W: 17.577
    return getLatLngBounds(-34.968, 17.577,-32.968, 19.577);
}

function getBoundsNashville() {
    // N: 36.247, S: 36.087, E: -86.660, W: -86.900
    return getLatLngBounds(36.087, -86.900,36.247, -86.660);
}

function getBoundsBoston() {
    // N: 42.410, S: 42.310, E: -70.959, W: -71.159
    return getLatLngBounds(42.310, -71.159,42.410, -70.959);
}

function getBounds(city) {
    if(city == 'nyc')
        return getBoundsNyc();
    else if(city == 'dc')
        return getBoundsDc();
    else if(city == 'london')
        return getBoundsLondon();
    else if(city == 'capetown')
        return getBoundsCapetown();
    else if(city == 'nashville')
        return getBoundsNashville();
    else if(city == 'boston')
        return getBoundsBoston();
    else
        return getBoundsUS();
}

function inProperBounds(tweet) {
    var bounds = null;
    if(getCity() == 'nyc')
		bounds = getBoundsNyc();
	else if(getCity() == 'dc')
		bounds = getBoundsDc();
	else if(getCity() == 'london')
	    bounds = getBoundsLondon();   
	else if(getCity() == 'capetown')
		bounds = getBoundsCapetown();
	else if(getCity() == 'nashville')
	    bounds = getBoundsNashville();
	else if(getCity() == 'boston')
		bounds = getBoundsBoston();
	else
		bounds = getBoundsUS();
	return bounds.contains(tweet.position_);
}

function getView() {
    var pathname = window.location.pathname;
    return pathname.split('/')[1];
}