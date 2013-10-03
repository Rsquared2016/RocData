<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core"%><%
%><%@ attribute name="user" required="true" type="twitter4j.User"%><% 

%>id: "${user.id}",<%
%>name: "${user.screenName}",<%
%>profile_image_url: "${user.profileImageURL}"