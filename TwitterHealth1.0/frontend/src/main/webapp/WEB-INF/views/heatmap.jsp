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
	href="/css/heatmap.css" />
<link type="text/css" rel="stylesheet" media="screen"
	href="/css/choropleth.css" />
<link type="image/x-icon" rel="icon" href="/css/images/favicon.ico" />
<link type="image/x-icon" rel="shortcut" href="/css/images/favicon.ico" />
<%@include file="logging.jsp"%>
<script type="text/javascript"
	src="http://cdnjs.cloudflare.com/ajax/libs/d3/2.10.0/d3.v2.min.js"></script>
<script type="text/javascript"
	src="http://maps.google.com/maps/api/js?v=3.9&sensor=true"></script>
<script type="text/javascript" src="/js/lib/date.js"></script>
<script type="text/javascript" src="/js/lib/geoxml3.js"></script>
<script type="text/javascript" src="/js/lib/jquery.js"></script>
<script type="text/javascript" src="/js/lib/jquery.min.js"></script>
<script type="text/javascript" src="/js/lib/jquery.ui.js"></script>
<script type="text/javascript" src="/js/lib/jquery.ui.custom.js"></script>
<script type="text/javascript" src="/js/lib/underscore.js"></script>
<script type="text/javascript" src="/js/common/heatmap.js"></script>
<script type="text/javascript" src="/js/common/heatmap-gmaps.js"></script>
<script type="text/javascript" src="/js/common/pollutants.js"></script>
<script type="text/javascript" src="/js/common/rtree.js"></script>
<script type="text/javascript" src="/js/common/swap.js"></script>
<script type="text/javascript" src="/js/common/choropleth.js"></script>
<script type="text/javascript" src="/js/pollution/about.js"></script>
<script type="text/javascript">
    (function() {
        _
            .mixin({
                // mixin JSP page objs so they are accessible outside this file
                getCurrentDay: function() {
                    return '${currentDay}';
                },
                getPreviousDay: function() {
                    return '${previousDay}';
                },
                getPreviousDayLink: function() {
                    return "<a href='<c:url value="${previousDay}"></c:url>'>Previous Day</a>";
                },
                getNextDay: function() {
                    return '${nextDay}';
                },
                getNextDayLink: function() {
                    return "<a href='<c:url value="${nextDay}"></c:url>'>Next Day</a>";
                },
                getCurrencDay: function() {
                    return '${currentDay}';
                },
                getCurrentDayLink: function() {
                    return '<c:url value="' + this.getCurrentDay() + '/data"></c:url>';
                }
            });
    })();
</script>
<script data-main="/js/heatmap/main" src="/js/lib/require.js"></script>
</head>

<body>
	<div id="map_canvas">
		<div id="loading-div">Loading data...</div>
	</div>
	<%@include file="google-analytics.jsp"%>
</body>

</html>