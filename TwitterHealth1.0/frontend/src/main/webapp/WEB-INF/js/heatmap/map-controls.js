define(["templates", "map"], function(templates, map) {
    
    controls = function() {
        this.templates = templates;
        this.create();
    };
    
    controls.prototype.create = function() {
        
        // time display
        this.clockControl = templates.createTextControl({
            text: "Time: 00:00"
        });
        
        // previous day
        this.previousDayControl = this.templates.createTextControl({
            text: _.getPreviousDayLink()
        });
        
        // next day
        this.nextDayControl = this.templates.createTextControl({
            text: _.getNextDayLink()
        });
        
        // current day
        this.currentDayControl = this.templates.createTextControl({
            text: _.getCurrentDay()
        });
        
        // time window
        this.timeWindowBtn = this.templates.createButton({
            text: "Time Window"
        });
        
        // traffic
        var trafficLayer = new google.maps.TrafficLayer();
        var trafficControl = this.templates.createTrafficControl();
        var legend = $(".gmap-control-legend", trafficControl);
        $(legend).hide();
        
        // Set hover toggle event
        $(trafficControl).mouseenter(function() {
            $(legend).show();
        }).mouseleave(function() {
            $(legend).hide();
        });
        
        $(trafficControl).click(
            function() {
                if (typeof trafficLayer.getMap() == 'undefined'
                    || trafficLayer.getMap() === null) {
                    $(trafficControl).addClass('gmap-control-active');
                    trafficLayer.setMap(require("map").gmap);
                } else {
                    trafficLayer.setMap(null);
                    $(trafficControl).removeClass('gmap-control-active');
                }
            });
        
        this.trafficControl = trafficControl;
    };
    
    return new controls();
    
});
