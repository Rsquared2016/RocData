
function PinSliderControl(timeDisplay) {
	// initialize slider divs
	this.sliderContainer = document.createElement('div');
	this.sliderTweets = document.createElement('div');
	this.timeDisplay = timeDisplay;
	this.active = true;
	$(this.sliderContainer).attr('id', 'sliderContainer');
	$(this.sliderTweets).attr('id', 'sliderTweets');
	$(this.sliderContainer).append(this.sliderTweets);
	// style
	this.sliderContainer.style.width = '400px';
	this.sliderContainer.style.paddingRight = '10px';
	this.sliderContainer.style.paddingTop = '10px';
	
	// create slider, set events
	this.dateRange = dateRanges[getCity()];
	var diff = (this.dateRange.first.getTime() - this.dateRange.last.getTime()) * 12 / 86400000;
	$(this.sliderTweets).slider({
		max: 0,
		min: diff,
		step: 12
	});
	
	// set default start positions
	$(this.sliderTweets).slider('option', 'value', diff);
	$("#sliderVal_hold").html('' + diff);
	
	// event handlers
	var context = this;
	$(this.sliderContainer).bind('click', function(event) {
		if(!context.active) {
			event.stopImmediatePropagation();
		}
	})
	
	$(this.sliderTweets).bind('slide', function(event, ui) {
		// get value,  make sure time is shown 
		var val = ui.value;
		showDate(timeDisplay, val);
	});
	
	$(this.sliderTweets).bind('slidechange', function(event, ui) {
	    // fix step size
		var slideStep = $(this).slider('option', 'step');
		if(ui.value <= -12 && slideStep != 12) {
		    $(this).slider('option', 'step', 12);
		    // reset the value (the slider will snap it to the right step now)
		    $(this).slider('value', ui.value);
	    }
	    
	    // update div value
		$("#sliderVal_hold").html('' + ui.value);
		
		// redraw old pins
		if(!!allTweets[getCity()]) {
            $.each(allTweets[getCity()], function(id, tweet) {
                tweet.draw();
            });
		}
		
		showDate(timeDisplay, ui.value);
		// fade out date display
		setTimeout(function() {
			$(timeDisplay.timeOverlay).effect('fade', {}, 1000);
		}, 500);
	});
	
	// not sure that this is necessary really
	this.sliderContainer.index = 1;
	allControls['pinSlider'] = this;
}

function TimeDisplay() {
	// add time display overlay
	this.timeOverlay = document.createElement('div');
	$(this.timeOverlay).attr('id', 'timeOverlay');
	// style
	this.timeOverlay.style.width = '400px';
	this.timeOverlay.style.paddingRight = '10px';
	this.timeOverlay.style.fontSize = '20px';
	this.timeOverlay.style.textAlign = 'center';
	this.timeOverlay.style.color = '#FFFFFF';
	
	// not sure if this is necessary
	this.timeOverlay.index = 1;
	allControls['timeDisplay'] = this;
}

function TimeControls(pinSlider, timeDisplay) {
	// initialize component divs
	this.pinSlider = pinSlider;
	this.timeDisplay = timeDisplay;
	this.state = 'pause';
	this.active = true;
	this.playTimeout = null;
	this.timeControlsContainer = document.createElement('div');
	this.backControl = document.createElement('div');
	this.pauseControl = document.createElement('div');
	this.playControl = document.createElement('div');
	this.forwardControl = document.createElement('div');
	$(this.timeControlsContainer).append(this.backControl);
	$(this.timeControlsContainer).append(this.pauseControl);
	$(this.timeControlsContainer).append(this.playControl);
	$(this.timeControlsContainer).append(this.forwardControl);
	// style
	this.timeControlsContainer.style.width = '400px';
	$(this.timeControlsContainer).children().css('float', 'left');
	$(this.timeControlsContainer).children().css('margin-left', '42px');
	$(this.timeControlsContainer).children().css('margin-right', '42px');
	$(this.timeControlsContainer).children().css('margin-top', '8px');
	$(this.timeControlsContainer).children().css('margin-bottom', '8px');
	$(this.timeControlsContainer).children().addClass('ui-icon');
	$(this.backControl).addClass('ui-icon-seek-prev');
	$(this.pauseControl).addClass('ui-icon-pause');
	$(this.playControl).addClass('ui-icon-play');
	$(this.forwardControl).addClass('ui-icon-seek-next');
	
	// event handlers
	var timeControl = this; // for closure purposes
	
	google.maps.event.addDomListener(this.backControl, 'click', function() {
		if(timeControl.active) {
		    // pause if necessary
			if(timeControl.state == 'play') {
			    timeControl.pause();
			}
			// fix step size if need be
		    var slideStep = $(timeControl.pinSlider.sliderTweets).slider('option', 'step');
		    if(slideStep != 12)
        	    $(timeControl.pinSlider.sliderTweets).slider('option', 'step', 12);
			// one step back
            timeControl.backward();
		}
	});
	
	google.maps.event.addDomListener(this.pauseControl, 'click', function() {
		if(timeControl.active) {
		    // fix step size if need be
		    var slideStep = $(timeControl.pinSlider.sliderTweets).slider('option', 'step');
		    if(slideStep != 12)
        	    $(timeControl.pinSlider.sliderTweets).slider('option', 'step', 12);
        	
			timeControl.pause();
		}
	});
	
	google.maps.event.addDomListener(this.playControl, 'click', function() {
		if(timeControl.active) {
			var slideVal = parseInt($(timeControl.pinSlider.sliderTweets).slider('value'));
			if(timeControl.state != 'play' && slideVal < 0) {
				timeControl.state = 'play';
				$(timeControl.timeDisplay.timeOverlay).show();
				setTimeout(function() {
					$(timeControl.timeDisplay.timeOverlay).effect('fade', {}, 1000);
				}, 500);
				
				timeControl.playTimeout = setTimeout(function() {
					playLoop(timeControl);
				}, 2000);
			}
		}
	});
	
	google.maps.event.addDomListener(this.forwardControl, 'click', function() {
		if(timeControl.active) {
		    // pause if necessary
			if(timeControl.state == 'play') {
			    timeControl.pause();
			}
			// fix step size if need be
		    var slideStep = $(timeControl.pinSlider.sliderTweets).slider('option', 'step');
		    if(slideStep != 12)
        	    $(timeControl.pinSlider.sliderTweets).slider('option', 'step', 12);
			// one step forward
            timeControl.forward();
		}
	});
	
	// not sure if this is really necessary
	this.timeControlsContainer.index = 1;
	allControls['timeControls'] = this;
}

TimeControls.prototype.reset = function(name) {
    // adjust slider to new date range
    this.pinSlider.dateRange = dateRanges[name];
    var first = dateRanges[name].first, last = dateRanges[name].last;
    var diff = (first.getTime() - last.getTime()) * 12 / 86400000;
    $(this.pinSlider.sliderTweets).slider('option', 'min', diff);

    // set default start positions
    $(this.pinSlider.sliderTweets).slider('option', 'value', diff);
    $("#sliderVal_hold").html('' + diff);
}

TimeControls.prototype.backward = function() {
    // get current value and min
	var slideVal = parseInt($(this.pinSlider.sliderTweets).slider('value'));
	var slideMin = parseInt($(this.pinSlider.sliderTweets).slider('option', 'min'));
	var slideStep = parseInt($(this.pinSlider.sliderTweets).slider('option', 'step'));
	// skip day if it has no tweets
	var nextVal = slideVal - slideStep;
	var nextDay = this.getDate(slideVal - slideStep);
	var minDay = this.getDate(slideMin);
	var dayMs = 86400000;
	while($.inArray(nextDay.toDateString(), daysWithTweets[getCity()]) == -1 &&
	        nextDay.getTime() >= minDay.getTime()) {
	    nextDay.setHours(23, 59, 59, 999);
	    nextDay.setTime(nextDay.getTime() - dayMs);
	    var dayDiff = (this.getDate() - nextDay.getTime()) / dayMs;
    	nextVal = slideVal - dayDiff * 12;
	}

	// if we can go backward, do it
	if(slideVal > slideMin) {
		$(this.pinSlider.sliderTweets).slider('value', nextVal);
	}
}

TimeControls.prototype.forward = function() {
    // get current value and max
	var slideVal = parseInt($(this.pinSlider.sliderTweets).slider('value'));
	var slideMax = parseInt($(this.pinSlider.sliderTweets).slider('option', 'max'));
	// if we are playing and we're at today, animate every 2 hrs
	var slideStep = parseInt($(this.pinSlider.sliderTweets).slider('option', 'step'));
	// skip day if it has no tweets
	var nextVal = slideVal + slideStep;
	var nextDay = this.getDate(slideVal + slideStep);
	var maxDay = this.getDate(slideMax);
	var dayMs = 86400000;
	while($.inArray(nextDay.toDateString(), daysWithTweets[getCity()]) == -1 &&
	        nextDay.getTime() <= maxDay.getTime()) {
	    nextDay.setHours(23, 59, 59, 999);
	    nextDay.setTime(nextDay.getTime() + dayMs);
	    var dayDiff = (nextDay.getTime() - this.getDate()) / dayMs;
    	nextVal = slideVal + dayDiff * 12;
	}

	// if we can go forward, do it
	if(slideVal < slideMax) {
		$(this.pinSlider.sliderTweets).slider('value', nextVal);
	}
}

TimeControls.prototype.pause = function() {
    // if it is playing, stop it
	if(this.state == 'play') {
		this.state = 'pause';
		if(!!this.playTimeout) {
			clearTimeout(this.playTimeout);
			this.playTimeout = null;
		}
	}
}

TimeControls.prototype.getDate = function(v) {
	var slideVal = v != null ? v : parseInt($(this.pinSlider.sliderTweets).slider('value'));
	var daysMs = slideVal * 2 * 60 * 60 * 1000;
	var todayMidnight = this.pinSlider.dateRange.last;
	return new Date(todayMidnight.getTime() + daysMs);
}

function playLoop(timeControl) {
	var slideVal = parseInt($(timeControl.pinSlider.sliderTweets).slider('value'));
	var slideEnd = parseInt($(timeControl.pinSlider.sliderTweets).slider('option', 'max'));
	var slideStep = parseInt($(timeControl.pinSlider.sliderTweets).slider('option', 'step'));
	
	if(slideVal >= slideEnd) {
		timeControl.state = 'pause';
		timeControl.playTimeout = null;
		return;
	}
	
	// switch step to 1 when we are on the last day
	if(slideVal >= -12 && slideVal < 0 && slideStep != 1) {
	    $(timeControl.pinSlider.sliderTweets).slider('option', 'step', 1);
	}
	
	timeControl.forward();
	$(timeControl.timeDisplay.timeOverlay).show();
	setTimeout(function() {
		$(timeControl.timeDisplay.timeOverlay).effect('fade', {}, 1000);
	}, 500);
	
	timeControl.playTimeout = setTimeout(function() {
		playLoop(timeControl);
	}, 2000);
}

function showDate(timeDisplay, val) {
	$(timeDisplay.timeOverlay).show();
	// calculate current date and display accordingly
	var daysMs = val * 2 * 60 * 60 * 1000;
	var todayMidnight = dateRanges[getCity()].last;
	var otherDay = new Date(todayMidnight.getTime() + daysMs);
	var timeStr = val >= -12 && val <= 0 ? otherDay.toString() : otherDay.toDateString();
	$(timeDisplay.timeOverlay).html(timeStr);
}
