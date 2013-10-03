
function CitySelector(map) {
    // initialize
    this.map = map;
    this.container = document.createElement('div');
    this.citySelect = document.createElement('select');
    // style
    this.container.style.width = '98px';
    this.container.style.margin = '12px';
    this.container.style.position = 'absolute';
    $(this.container).append(this.citySelect);
    
    // add options
    var context = this;
    var cities = {
        boston: 'Boston',
        nyc:    'New York City'
    };
    
    // only show NYC and Boston when page is /health
    $.each(cities, function(abbrev, city) {
        $(context.citySelect).append('<option value="' + abbrev + '">' + city + '</option>');
        if(abbrev == defaultCity)
            $(context.citySelect).children().last().attr('selected', 'selected');
    });
    
    // event handlers
    $(this.citySelect).change(function(event) {
        var newCity = $(this).val();
        // focus on new city in map
        onLoad_map(context.map, event);
        if(!!activeInfoWindow) {
            activeInfoWindow.close();
            activeInfoWindow = null;
        }
        // get JSON for city if we made a new selection
        if(!allTweets[newCity]) {
            progressiveLoad(newCity);
        }
        else {
            $.each(allTweets[newCity], function(i, tweet) { tweet.setMap(context.map); });
        }
        // reset slider
        allControls['timeControls'].reset(newCity);
        // enable or disable tutorial
        if($(this).val() == 'nyc') {
            $(allControls.tutorialButton.buttonDiv).removeClass('ui-state-disabled');
            $.each(allControls.pollutantButtons, function(name, button) {
                $(button).removeClass('ui-state-disabled');
            });
        }
        else {
            $(allControls.tutorialButton.buttonDiv).addClass('ui-state-disabled');
            $.each(allControls.pollutantButtons, function(name, button) {
                $(button).addClass('ui-state-disabled');
            });
        }
        // remove old pins, add new ones
        // naive: just reset all pins, but find a better way to do this
        $.each(allTweets, function(city, tweets) {
            if(city == newCity)
                $.each(tweets, function(id, tweet) { tweet.setMap(context.map); });
            else
                $.each(tweets, function(id, tweet) { tweet.setMap(null); });
        });
    });
    
    allControls['citySelect'] = this;
}