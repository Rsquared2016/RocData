var allControls = {};

define(
    ["map-options", "heatmap-options", "map-util", "templates", "map-controls",
            "../common/player-control"],
    function(mapOptions, heatmapOptions, mapUtil, templates, controls, PlayerControl) {
        
        map = function() {
            this.tasks = [];
        };
        
        map.prototype = {
            
            init: function() {
                
                var self = this;
                
                var currentDayControlDiv = controls.currentDayControl;
                var timeWindowBtn = controls.timeWindowBtn;
                
                // traffic overlay control
                var trafficControl = controls.trafficControl;
                
                var map = new google.maps.Map(document.getElementById("map_canvas"),
                    mapOptions);
                self.gmap = map;
                
                map.fitBounds(mapUtil.getNyBounds());
                
                // pollutants overlay
                var pollutantButtons = new PollutantControls(map);
                
                // heatmap
                var heatmap = new HeatmapOverlay(map, heatmapOptions);
                self.heatmap = heatmap;
                
                // toggle time window
                $(timeWindowBtn).click(function() {
                    heatmap.toggleTimeWindow();
                });
                
                var aboutButton = new AboutButton(map);
                var swapButton = new SwapPagesButton(map);
                var playerControl = new PlayerControl(heatmap);
                
                // add heatmap controls
                map.controls[google.maps.ControlPosition.LEFT_TOP]
                    .push(aboutButton.window.window);
                map.controls[google.maps.ControlPosition.TOP_CENTER]
                    .push(controls.clockControl);
                if (_.getPreviousDay()) {
                    var previousDayControlDiv = controls.previousDayControl;
                    map.controls[google.maps.ControlPosition.TOP]
                        .push(previousDayControlDiv);
                }
                map.controls[google.maps.ControlPosition.TOP].push(currentDayControlDiv);
                if (_.getNextDay()) {
                    var nextDayControlDiv = controls.nextDayControl;
                    map.controls[google.maps.ControlPosition.TOP].push(nextDayControlDiv);
                }
                map.controls[google.maps.ControlPosition.LEFT_BOTTOM]
                    .push(pollutantButtons.buttonsContainer);
                map.controls[google.maps.ControlPosition.LEFT_BOTTOM]
                    .push(aboutButton.button);
                map.controls[google.maps.ControlPosition.LEFT_BOTTOM].push(timeWindowBtn);
                map.controls[google.maps.ControlPosition.LEFT_BOTTOM]
                    .push(trafficControl);
                map.controls[google.maps.ControlPosition.RIGHT_BOTTOM]
                    .push(swapButton.button);
                map.controls[google.maps.ControlPosition.TOP]
                    .push(playerControl.controlDiv);
                
                // handlers
                var hin = function(event) {
                    $(this).css('cursor', 'pointer');
                };
                var hout = function(event) {
                    $(this).css('cursor', 'default');
                };
                
                // add to individual controls
                $(aboutButton.button).hover(hin, hout);
                $(aboutButton.window.closeButton).hover(hin, hout);
                $(trafficControl).hover(hin, hout);
                $.each(pollutantButtons, function(name, button) {
                    $(button).hover(hin, hout);
                });
                $(swapButton.button).hover(hin, hout);
                $(timeWindowBtn).hover(hin, hout);
                
                self.fetchData();
            },
            
            fetchData: function() {
                var self = this;
                $.getJSON(_.getCurrentDayLink(), function(data) {
                    var dataSet = data ? data : {
                        data: []
                    };
                    log.info("loaded " + dataSet.length + " tweets");
                    self.heatmap.setDataSet(dataSet);
                    self.heatmap.forceDraw();
                });
            }
        
        };
        
        return new map();
        
    });
