<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core"%>
<%@ taglib prefix="fn" uri="http://java.sun.com/jsp/jstl/functions"%>

<head>
<title>${title}</title>
<meta name="viewport"
	content="width=device-width, initial-scale=1.0, user-scalable=no">

<c:if test="${include != 'mobile.jsp'}">
	<link type="text/css" rel="stylesheet" media="screen"
		href="/wro/global.css<%//?minimize=false%>" />
</c:if>
<c:if test="${include == 'mobile.jsp'}">
	<link type="text/css" rel="stylesheet" media="screen"
		href="/wro/mobile.css<%//?minimize=false%>" />
</c:if>
<c:if
	test="${include == 'heatmap.jsp' || include == 'pollution.jsp' || include == 'health.jsp'}">
	<link type="text/css" rel="stylesheet" media="screen"
		href="/wro/${fn:substring(include, 0, fn:length(include) - 4)}.css<%//?minimize=false%>" />
</c:if>
<c:if test="${fn:startsWith(include, '../static')}">
	<link type="text/css" rel="stylesheet" media="screen"
		href="/wro/paledot.css<%//?minimize=false%>" />
</c:if>
<!-- <c:if test="${include == '../static/about.jsp'}">
        <link type="text/css" rel="stylesheet" media="screen" href="/wro/about.css<%//?minimize=false%>"/>
    </c:if> -->

<link type="image/x-icon" rel="icon" href="/css/images/favicon.ico" />
<link type="image/x-icon" rel="shortcut" href="/css/images/favicon.ico" />
<meta name="google-site-verification" content="3NjOgq0OUx9DXQGAnncn4jOwoNskD-dpQH8q_JTWYf0" />
</head>
