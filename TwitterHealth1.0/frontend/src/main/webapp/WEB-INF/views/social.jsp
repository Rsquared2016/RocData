<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core"%>
<%@ taglib prefix="fountin" tagdir="/WEB-INF/tags"%>
<!DOCTYPE html>
<html>

<head>
<title>${title}</title>
<meta name="viewport"
	content="width=device-width, initial-scale=1.0, user-scalable=no">
<link type="text/css" rel="stylesheet" media="screen"
	href="/wro/global.css" />
<link type="image/x-icon" rel="icon" href="/css/images/favicon.ico" />
<link type="image/x-icon" rel="shortcut" href="/css/images/favicon.ico" />
<script type="text/javascript"
	src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.4/jquery.min.js"></script>
<script type="text/javascript"
	src="http://maps.google.com/maps/api/js?v=3.9&sensor=true"></script>
<script type="text/javascript" src="/js/lib/jquery.min.js"></script>
<script type="text/javascript" src="/js/lib/map.js"></script>
<script type="text/javascript" src="/js/lib/jquery.ui.js"></script>
<%@include file="logging.jsp"%>
</head>

<body>
	<form action='/social' style='clear: left; margin: 20px'>
		<select name='name'>
			<option value="">Please Select..</option>
			<c:forEach items="${page}" var="tweet">
				<fountin:tweet2 tweet="${tweet}" />
			</c:forEach>
		</select> <input type='submit' />
	</form>
	<%
	    if (request.getParameter("name") != null) {
	%><div id="map_canvas"
		style="position: absolute !important; width: 100%; top: 62px; bottom: 40px">
		<div style="margin: 30% auto; text-align: center">Starting
			location services...</div>
	</div>
	<%
	    }
	%><div id="the-map" style="float: left; clear: both">
		<c:choose>
			<c:when test="${empty page}">
				<p>fountin can't access twitter</p>
				<h2>
					<a href="new">Setup a System</a>
				</h2>
			</c:when>
			<c:otherwise>
				<%
				    if (request.getParameter("name") != null) {
				%>
				<c:forEach items="${page}" var="tweet">
					<fountin:tweet1 tweet="${tweet}" />
				</c:forEach>
				<%
				    }
				%>
			</c:otherwise>
		</c:choose>
	</div>
	<script type="text/javascript">
        var meLoc, map;
        $(document).ready(
            function() {
                var lat, lng;
                
                //find the location of target user
                $.each($('.tweet'), function() {
                    if ($(this).attr('core') == 'yes') {
                        lat = parseFloat($(this).attr('lat'));
                        lng = parseFloat($(this).attr('lng'));
                        meLoc = new google.maps.LatLng(lat, lng);
                        //draw the map
                        tempMap = draw();
                        //add the pin
                        new google.maps.Marker({
                            position: meLoc,
                            map: map,
                            title: "Hello World!"
                        });
                    }
                });
                
                //get the nearby users
                $.each($('.tweet'), function() {
                    var temp_lat = parseFloat($(this).attr('lat'));
                    var temp_lng = parseFloat($(this).attr('lng'));
                    var lat_diff = Math.abs(temp_lat - lat);
                    var lng_diff = Math.abs(temp_lng - lng);
                    if (lat_diff > 0.05 || lng_diff > 0.05)
                        $(this).hide();
                    else {
                        $(this).show();
                        var tempLoc = new google.maps.LatLng(temp_lat, temp_lng);
                        //add the pin
                        addPin(tempLoc, $(this).attr('health'));
                        addLine(meLoc, tempLoc, parseFloat($(this).attr('health')));
                    }
                });
                
                //add the thing to show up on the map
                $.each($('.container'), function() {
                    $(this).parent().append(
                        $('<div class="tweetInfo"></div>').html(
                            $(this).clone().attr("class", "snippet")));
                });
                
            });// end document.ready()
        function draw() {
            var myOptions = {
                center: meLoc,
                zoom: 13,
                mapTypeId: google.maps.MapTypeId.ROADMAP
            };
            map = new google.maps.Map(document.getElementById("map_canvas"), myOptions);
            var darkStyles = [{
                stylers: [{
                    invert_lightness: true
                }, {
                    saturation: -56
                }, {
                    lightness: -56
                }, {
                    visibility: "simplified"
                }]
            }, {
                featureType: "road",
                stylers: [{
                    visibility: "simplified"
                }, {
                    lightness: -34
                }, {
                    saturation: -44
                }, {
                    hue: "#00f6ff"
                }]
            }, {
                featureType: "road",
                elementType: "labels",
                stylers: [{
                    visibility: "off"
                }]
            }, {
                featureType: "water",
                stylers: [{
                    hue: "#0066ff"
                }, {
                    invert_lightness: true
                }, {
                    saturation: -68
                }, {
                    lightness: -71
                }]
            }];
            map.setOptions({
                styles: darkStyles
            });
            return map;
        }

        function addPin(loc, opacity) {
            var opacityY = Math.abs(Math.floor((opacity - 1 + .16) * 200 * 10101));
            var circleOptions = {
                strokeColor: "#" + opacityY,
                strokeOpacity: (opacity - 0.84) * 2,
                strokeWeight: 1,
                fillColor: convert(opacity),//"#"+opacityY,
                fillOpacity: (opacity - 0.84) * 2,
                map: map,
                center: loc,
                radius: 150,
            };
            cityCircle = new google.maps.Circle(circleOptions);
            //add event
            google.maps.event.addListener(cityCircle, 'click', function() {
                //alert("want to see people around "+loc+"?");
                $.each($('.tweet'), function() {
                    var new_lat = loc.lat();
                    var new_lng = loc.lng();
                    var newLoc = new google.maps.LatLng(new_lat, new_lng);
                    var temp_lat = parseFloat($(this).attr('lat'));
                    var temp_lng = parseFloat($(this).attr('lng'));
                    var lat_diff = Math.abs(temp_lat - new_lat);
                    var lng_diff = Math.abs(temp_lng - new_lng);
                    if (lat_diff > 0.05 || lng_diff > 0.05)
                        ;
                    else {
                        //$(this).show();
                        var tempLoc = new google.maps.LatLng(temp_lat, temp_lng);
                        //add the pin
                        addPin(tempLoc, $(this).attr('health'));
                        addLine(newLoc, tempLoc, parseFloat($(this).attr('health')));
                    }
                });
            });
            //var marker = new google.maps.Marker({
            //position: loc,
            //map: map,
            //});
        }
        function addLine(start, end, opacity) {
            var opacityY = Math.abs(Math.floor((opacity - 1 + .16) * 200 * 10101));
            var flightPlanCoordinates = [start, end, ];
            var flightPath = new google.maps.Polyline({
                path: flightPlanCoordinates,
                strokeColor: convert(opacity),//'#'+opacityY,
                strokeOpacity: (opacity - 1 + 0.16) * 4,
                strokeWeight: 3
            });
            
            flightPath.setMap(map);
        }
        function convert(opacity) {
            if (opacity < 0.82)
                return "#BBFF33";
            else if (opacity < 0.84)
                return "#CCFF66";
            else if (opacity < 0.86)
                return "#DDFF99";
            else if (opacity < 0.88)
                return "#EEFFCC";//
            else if (opacity < 0.90)
                return "#FFFFCC";
            else if (opacity < 0.92)
                return "#FFFF99";
            else if (opacity < 0.94)
                return "#FFFF66";
            else if (opacity < 0.96)
                return "#FFFF33";
            else if (opacity < 0.98)
                return "#FFFF00";//
            else if (opacity < 1)
                return "#FFEECC";
            else if (opacity < 1.02)
                return "#FFDD99";
            else if (opacity < 1.04)
                return "#FFCC66";
            else if (opacity < 1.06)
                return "#FFBB33";
            else if (opacity < 1.08)
                return "#FFAA00";//
            else if (opacity < 1.1)
                return "#FF7733";
            else if (opacity < 1.12)
                return "#D94426";
            else if (opacity < 1.14)
                return "#Ed3B19";
            else if (opacity < 1.16)
                return "#F2330D";
            else
                return "#FF0000";
        }
    </script>
	<%@include file="google-analytics.jsp"%>
</body>