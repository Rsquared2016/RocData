<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core"%>
<!DOCTYPE html>

<html>
<c:url value="/experimental/distances/park/data" var="parksURL"></c:url>
<c:url value="/experimental/distances/gym/data" var="gymsURL"></c:url>

<head>
<meta name="viewport" content="initial-scale=1.0, user-scalable=no" />
<link type="text/css" rel="stylesheet" media="screen"
	href="/resources/styles/distances.css" />
<script type="text/javascript"
	src="http://maps.google.com/maps/api/js?v=3.9&sensor=true"></script>
<script type="text/javascript" src="/resources/scripts/jquery.js"></script>
<script type="text/javascript"
	src="/resources/scripts/jquery.ui.custom.js"></script>
<script type="text/javascript"
	src="/resources/scripts/layers/CombinedLayersOverlay.js"></script>
<script type="text/javascript"
	src="/resources/scripts/layers/DistanceHeatmap.js"></script>
<script type="text/javascript"
	src="/resources/scripts/log4javascript.js"></script>
<script type="text/javascript">
    var log = log4javascript.getLogger();
    var consoleAppender = new log4javascript.BrowserConsoleAppender();
    log.addAppender(consoleAppender);

    // DataSource
    function DataSource(name, url, cached) {
        this.url = url;
        this.cached = cached;
        this.name = name;
    };

    DataSource.prototype.initData = function(initCallback) {
        if (this.cached && this.data) {
            log.info("using cached data for " + this.name);
            initCallback();
            return;
        }
        var me = this;
        log.info("loading data from " + this.url);
        $.getJSON(this.url, function(data) {
            me.data = data;
            initCallback();
        });
    };

    function init() {
        log.info("initializing page...");
        var options = {
            center : new google.maps.LatLng(-34.397, 150.644),
            zoom : 8,
            mapTypeId : google.maps.MapTypeId.ROADMAP
        };

        var map = new google.maps.Map(document.getElementById("map_canvas"),
                options);

        // fit map into NY area
        var psw = new google.maps.LatLng(40.467597, -74.409908);
        var pne = new google.maps.LatLng(41.046156, -73.548989);
        var nybounds = new google.maps.LatLngBounds(psw, pne);
        map.fitBounds(nybounds);

        var overlay = new CombinedLayersOverlay(map, {
            globalAlpha : 0.4
        });

        var dataSourceList = [];

        var parkDataSource = new DataSource("parks", "${parksURL}", true);
        var gymDataSource = new DataSource("gyms", "${gymsURL}", true);
        dataSourceList.push(parkDataSource);
        dataSourceList.push(gymDataSource);

        var parkDistanceHeatmap = new DistanceHeatmap("parksHeatmap", {
            radius : 300000,
            color : {
                r : 0,
                g : 0,
                b : 255
            }
        }, parkDataSource);

        var gymDistanceHeatmap = new DistanceHeatmap("gymsHeatmap", {
            radius : 300000,
            color : {
                r : 255,
                g : 0,
                b : 0
            }
        }, gymDataSource);

        $("#btnParks").click(function() {
            var type = "park";
            var heatmap = parkDistanceHeatmap;
            var dataSource = parkDataSource;
            if (!dataSource.data)
                dataSource.initData(function() {
                    heatmap.addMarkers(map, dataSource.data, type);
                });
            else {
                if (!heatmap.hasMarkers(type))
                    heatmap.addMarkers(map, dataSource.data, type);
                else
                    heatmap.toggleMarkers(type);
            }
        });

        $("#btnParksHeatmap").click(function() {
            var dataSource = parkDataSource;
            dataSource.initData(function() {
                overlay.drawLayers({
                    mode : "graphical"
                }, [ parkDistanceHeatmap ]);
            });
        });

        $("#btnGyms").click(function() {
            var type = "gym";
            var heatmap = gymDistanceHeatmap;
            var dataSource = gymDataSource;
            if (!dataSource.data)
                dataSource.initData(function() {
                    heatmap.addMarkers(map, dataSource.data, type);
                });
            else {
                if (!heatmap.hasMarkers(type))
                    heatmap.addMarkers(map, dataSource.data, type);
                else
                    heatmap.toggleMarkers(type);
            }
        });

        $("#btnGymsHeatmap").click(function() {
            var dataSource = gymDataSource;
            dataSource.initData(function() {
                overlay.drawLayers({
                    mode : "graphical"
                }, [ gymDistanceHeatmap ]);
            });
        });

        $("#btnDrawHeatmaps").click(function() {
            var len = dataSourceList.length;
            var numReady = 0;
            var counter = len;

            while (counter--) {
                var dataSource = dataSourceList[counter];
                dataSource.initData(function() {
                    numReady++;
                    if (numReady == len) {
                        overlay.drawLayers({
                            mode : "graphical"
                        }, [ parkDistanceHeatmap, gymDistanceHeatmap ]);
                    }
                });
            }
        });

        google.maps.event.addDomListener(window, "resize", function() {
            overlay.onResize();
        });
    }
</script>

</head>

<body onload="init()">
	<button id="btnParks">Parks - pins</button>
	<button id="btnParksHeatmap">Parks - heatmap</button>
	<button id="btnGyms">Gyms - pins</button>
	<button id="btnGymsHeatmap">Gyms - heatmap</button>
	<button id="btnDrawHeatmaps">Combined heatmaps</button>
	<div id="map_canvas"></div>
</body>
</html>