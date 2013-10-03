<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core"%>
<!DOCTYPE html>
<html>

<head>
<title>${title}</title>
<meta name="viewport"
	content="width=device-width, initial-scale=1.0, user-scalable=no">
<link type="text/css" rel="stylesheet" media="screen"
	href="/wro/global.css" />
<link type="text/css" rel="stylesheet" media="screen"
	href="/css/style-dev0.css" />
<link type="text/css" rel="stylesheet" media="screen"
	href="/css/choropleth.css" />
<link type="image/x-icon" rel="icon" href="/css/images/favicon.ico" />
<link type="image/x-icon" rel="shortcut" href="/css/images/favicon.ico" />
<%@include file="logging.jsp"%>
<script type="text/javascript"
	src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.4/jquery.min.js"></script>
<script type="text/javascript"
	src="http://cdnjs.cloudflare.com/ajax/libs/d3/2.10.0/d3.v2.min.js"></script>
<script type="text/javascript"
	src="http://maps.google.com/maps/api/js?v=3.9&sensor=true"></script>
<script type="text/javascript" src="/js/lib/jquery.min.js"></script>
<script type="text/javascript" src="/js/lib/map.js"></script>
<script type="text/javascript" src="/js/lib/date.js"></script>
<script type="text/javascript" src="/js/lib/jquery.ui.js"></script>
<script type="text/javascript" src="/js/lib/jquery.ui.custom.js"></script>
<script type="text/javascript" src="/js/lib/geoxml3.js"></script>
<script type="text/javascript" src="/js/lib/ProjectedOverlay.js"></script>
<script type="text/javascript">
    (function() {
        window.api = '${api}';
        window.defaultCity = '${defaultCity}';
    })();
</script>
<script type="text/javascript" src="/js/common/choropleth.js"></script>
<script type="text/javascript" src="/js/common/rtree.js"></script>
<script type="text/javascript" src="/js/common/pin.js"></script>
<script type="text/javascript" src="/js/common/heatmap-gmaps.js"></script>
<script type="text/javascript" src="/js/common/heatmap.js"></script>
<script type="text/javascript" src="/js/common/pollutants.js"></script>
<script type="text/javascript" src="/js/common/swap.js"></script>
<script type="text/javascript" src="/js/pollution/pin_pollution.js"></script>
<script type="text/javascript" src="/js/pollution/initialize.js"></script>
<script type="text/javascript" src="/js/pollution/pin_slider.js"></script>
<script type="text/javascript" src="/js/pollution/tutorial.js"></script>
<script type="text/javascript" src="/js/pollution/about.js"></script>
<script type="text/javascript" src="/js/pollution/city_select.js"></script>
<script type="text/javascript" src="/js/pollution/map-pollution.js"></script>
</head>

<body>
	<div id="map_canvas">
		<div style="margin: 25% auto; text-align: center">Starting
			location services...</div>
	</div>
	<div id="pin_canvas" style="display: none;"></div>
	<div id="sliderVal_hold" style="display: none;">0</div>

	<div id="pageSwitch">
		<div id="prevLink"></div>
		<div id="nextLink"></div>
	</div>
	<%@include file="google-analytics.jsp"%>
</body>