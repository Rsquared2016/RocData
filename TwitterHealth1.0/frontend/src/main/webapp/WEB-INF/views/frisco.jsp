<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core"%>
<%@ taglib prefix="fountin" tagdir="/WEB-INF/tags/tweets"%>
<!DOCTYPE html>
<html>
<head>
<title>${title}</title>
<meta name="viewport"
	content="width=device-width, initial-scale=1.0, user-scalable=no">
<link rel="stylesheet" type="text/css" href="/css/styles/mobile.css">
<link type="text/css" rel="stylesheet" media="screen"
	href="/wro/global.css" />
<link type="image/x-icon" rel="icon" href="/css/images/favicon.ico" />
<link type="image/x-icon" rel="shortcut" href="/css/images/favicon.ico" />
<script type="text/javascript"
	src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.4/jquery.min.js"></script>
<script type="text/javascript"
	src="http://cdnjs.cloudflare.com/ajax/libs/d3/2.10.0/d3.v2.min.js"></script>
<script type="text/javascript"
	src="http://maps.google.com/maps/api/js?v=3.9&sensor=true"></script>
<%@include file="logging.jsp"%>
<script type="text/javascript" src="/js/lib/jquery.ui.custom.js"></script>
<script type="text/javascript" src="/js/lib/underscore.js"></script>
<script type="text/javascript" src="/js/lib/date.js"></script>
<script type="text/javascript" src="/js/lib/jquery.cookies.2.2.0.js"></script>
<script type="text/javascript">
(function() {
     // bootstrap tweet info 
     // CRITICAL ASSUMPTIONS:
     // I assumed that Status.person -> Tweet.fromperson 
     // and Status.in_reply_to_person -> Tweet.to_person 
     // note: Status is REST API, Tweet is search API
     var tweets = [];
     <c:forEach items="${tweets}" var="tweet">
     tweets.push({<fountin:geotagged-tweet tweet="${tweet}"/>});
     </c:forEach>
     var health_risk = <c:out value="${health_risk}">0.0</c:out>;
     var bootstrap = {
         health_risk: health_risk,
         tweets: tweets,
         user_id = "${person.id}"
     };
     
     window.bootstrap = bootstrap;
})();
</script>
<script data-main="/js/mobile/main" src="/js/lib/require.js"></script>
</head>
<body>
	<div class="mobile-header">
		<div id="panel_header">
			<!-- currently unavailable -->
			<c:if test="false">
				<div id="twttr">
					<a class="btn" style="float: none; clear: both; width: 100%;"
						href="oauth/twitter/authorize"> <img
						src="https://dev.twitter.com/sites/default/files/images_documentation/bird_blue_16.png">
						See what your friends are doing
					</a>
				</div>
			</c:if>
		</div>
	</div>
	<div class="mobile-body">
		<div class="mobile-view map-view">
			<div id="map_canvas"></div>
		</div>
	</div>
	<%@include file="google-analytics.jsp"%>
</body>
</html>
