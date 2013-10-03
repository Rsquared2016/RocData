<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core"%>
<!DOCTYPE html>
<html>

<head>
<title>${title}</title>
<meta name="viewport"
	content="width=device-width, initial-scale=1.0, user-scalable=no">
<meta name="Description" content="We analyze health at scale, using artificial intelligence that understands the language of social media. Track spread of germs in real time with our app!">
<link type="text/css" rel="stylesheet" media="screen"
	href="/wro/mobile.css<%//?minimize=false%>" />
<link type="image/x-icon" rel="icon" href="/css/images/favicon.ico" />
<link type="image/x-icon" rel="shortcut" href="/css/images/favicon.ico" />
<%@include file="logging.jsp"%>
<script type="text/javascript"
	src="http://ajax.googleapis.com/ajax/libs/jquery/1.8.2/jquery.min.js"></script>
<script type="text/javascript"
	src="http://maps.google.com/maps/api/js?v=3.9&sensor=true"></script>
<script type="text/javascript" src="/wro/mobile.js"></script>
<script type="text/javascript" src="/js/lib/jquery.cookies.2.2.0.js"></script>
<script data-main="/resources/js/mobile/main"
	src="/resources/js/lib/require.js"></script>
<script type="text/javascript">
    $(function() {
        $('#report_tab_text').on('swipeup', function() {
            alert('swiped');
        });
        $('#report_tab_text').on('movestart', function() {
            log.info('swiped');
        });
        // $('#report_tab_text').on('touchstart', function(){
        //   alert('touched');
        // });
    });
</script>
</head>

<body>
	<div class='navbar navbar-inverse navbar-fixed-top'>
		<div class='navbar-inner'>
			<div class='container'>
				<a href="/m" class='brand'>GermTracker</a>
				<ul class='nav pull-right'>
					<li><a href="/about">About</a></li>
					<li id='nav_divider' class='divider-vertical'></li>
					<li><a id='view_toggle_link' href="#">List <i
							class='icon-list icon-white'></i>
					</a></li>
				</ul>
			</div>
		</div>
	</div>

	<div id='main_container' class='container'>
		<div class='row'>
			<div class='span12'>
				<div class="mobile-body">
					<div id="overlay">
						<div id="map_overlay_text_wrapper">
							<div id="map_overlay_text">
								Health Risk: <span id="current_health_risk"></span>
							</div>
							<!-- <div id="important-message">We are experiencing heavy user traffic. Please excuse potential delays.</div>  -->
						</div>
						<div id="map_overlay_tweet_wrapper">
							<a href="https://twitter.com/share" class="twitter-share-button"
								data-text="Track the health risk of your area with GermTracker"
								data-related="fountin" data-count="none" data-dnt="true">Tweet</a>
							<script>
                                !function(d, s, id) {
                                    var js, fjs = d.getElementsByTagName(s)[0];
                                    if (!d.getElementById(id)) {
                                        js = d.createElement(s);
                                        js.id = id;
                                        js.src = "//platform.twitter.com/widgets.js";
                                        fjs.parentNode.insertBefore(js, fjs);
                                    }
                                }(document, "script", "twitter-wjs");
                            </script>
						</div>
						<div class="overlay_background"></div>
						<div class="solid_overlay_background"></div>
					</div>

					<div id="list_spacer"></div>
					<div class="mobile-view map-view">
						<div id="map_canvas"></div>
					</div>
				</div>
			</div>
		</div>
	</div>

	<div>
		<div id="report_tab_wrapper">
			<div id="report_tab_background"></div>
			<div id="report_tab_text">
				Report <i class='icon-arrow-up icon-white'></i>
			</div>
		</div>
	</div>
	<div class="modal hide"></div>
	<%@include file="google-analytics.jsp"%>
</body>

</html>
