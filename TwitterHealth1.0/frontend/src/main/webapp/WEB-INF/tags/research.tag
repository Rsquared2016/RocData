<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core"%>
<%@ attribute name="title" required="true" type="java.lang.String"%>
<%@ attribute name="file" required="true" type="java.lang.String"%>
<%@ attribute name="links" required="false" type="String[]" %>

<a href="/research/${file}.pdf">${title}</a> | <a href="/research/${file}_bibtex.txt">bibtex</a><%

int i=0;%>

Coverage: 
<c:forEach var="link" items="${links}"><%
	if(i%2==0){%><a href="${link}"><%
	}else{%>${link}</a> | <%}
	i++;
 %></c:forEach>