<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core"%><%
%><%@ taglib uri="http://java.sun.com/jsp/jstl/functions" prefix="fn" %><%
%><%@ attribute name="year" required="true" type="java.lang.String" %><%
%><%@ attribute name="page" required="false" type="java.lang.String" %><%

String site ="Fount.in";

%><c:if test="${
	page!='mobile.jsp' 
	and fn:startsWith(page, '../static') == false
   }"><%
	%><div id="footer"><%
		%><ul><%	
			%><li>&copy; ${year} <%=site%>, Inc</li> | <%
			%><li><a href="/about">about</a><%
		%></ul><%
	%></div><%
%></c:if><%

// logging
%><script type="text/javascript" src="/js/lib/log4javascript.js"></script>
<script type="text/javascript">
    var log = log4javascript.getLogger();
    var consoleAppender = new log4javascript.BrowserConsoleAppender();
    log.addAppender(consoleAppender);
</script><%

// google analytics
%><script type="text/javascript">
var _gaq = _gaq || [];
  _gaq.push(['_setAccount', 'UA-22485363-3']);
  _gaq.push(['_trackPageview']);

(function() {
    var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
    ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
    var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);
  })();
</script>
