<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core"%>
<%@ taglib prefix="fn" uri="http://java.sun.com/jsp/jstl/functions"%>
<%@ page import="java.util.Date, in.fount.util.CalendarUtils"%>
<!DOCTYPE html>
<html>
<head>
<title>${title}</title>
<meta name="viewport"
	content="width=device-width, initial-scale=1.0, user-scalable=no">
<link type="text/css" rel="stylesheet" media="screen"
	href="/wro/global.css" />
<link rel="stylesheet" type="text/css" href="/css/diseases.css">
<link type="image/x-icon" rel="icon" href="/css/images/favicon.ico" />
<link type="image/x-icon" rel="shortcut" href="/css/images/favicon.ico" />
<script type="text/javascript"
	src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.4/jquery.min.js"></script>
<script type="text/javascript"
	src="http://maps.google.com/maps/api/js?v=3.9&sensor=true"></script>
<script src="http://d3js.org/d3.v2.js"></script>
<%@include file="logging.jsp"%>
<script type="text/javascript" src="/js/lib/jquery.min.js"></script>
<script type="text/javascript" src="/js/lib/map.js"></script>
<script type="text/javascript" src="/js/lib/jquery.ui.js"></script>
<script type="text/javascript" src="/js/lib/jquery.ui.custom.js"></script>
<script type="text/javascript" src="/js/lib/geoxml3.js"></script>
<script type="text/javascript" src="/js/lib/ProjectedOverlay.js"></script>
<script type="text/javascript" src="/js/common/pin.js"></script>
<script type="text/javascript" src="/js/pollution/initialize.js"></script>
<script type="text/javascript" src="/js/diseases/histograms.js"></script>
<script type="text/javascript" src="/js/diseases/map-diseases.js"></script>
<script type="text/javascript">
    function isDiseasePage() {
        return "${disease}" != "";
    }

    function getDayPageName() {
        return "${day}";
    }

    function getHourPageName() {
        return "${hour}";
    }

    function getDiseasePageName() {
        return "${disease}";
    }

    function getTagPageName() {
        return "${tag}";
    }
</script>

</head>

<body>
	<div id="chart" style="width: 100%"></div>

	<div id="tweet_info" style="width: 100%">
		<div id="map_canvas"
			style="width: 100%; height: 25%; min-height: 350px; max-height: 350px; margin: auto; float: left">
			<div style="margin: 25% auto; text-align: center">Starting
				location services...</div>
		</div>
		<div id="loading_anim" = style="width: 100%; height: 19px">
			<img src="/css/images/pins-load.gif" width="220px" height="19px"></img>
		</div>
	</div>

	<form class='form'>
		<select
			onChange="if(this.selectedIndex!=0)
        self.location=this.options[this.selectedIndex].value">
			<option value="" selected>Select a day</option>
			<c:forEach var="day" items="${availableDays}">
				<option value="/diseases/${day}">${fn:replace(fn:substring(day,
					5, fn:length(day)), '-', '/')}</option>
			</c:forEach>
		</select>
	</form>
	<div id="bounds" style="font-size: 12px"></div>

	<ul id="histogram"></ul>
	<%@include file="google-analytics.jsp"%>
</body>

</html>
