<%@ taglib prefix="fountin" tagdir="/WEB-INF/tags" %><%
%><%@ taglib uri="http://java.sun.com/jsp/jstl/functions" prefix="fn" %><%
%><%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core"%><%

%><!DOCTYPE html><%

%><html ><%
	%><fountin:head/><%
	%><body><%
		%><jsp:include page="pages/${include}"/><%
		%><fountin:footer year="2012" page="${include}" /><%
	 %></body><%
%></html>
