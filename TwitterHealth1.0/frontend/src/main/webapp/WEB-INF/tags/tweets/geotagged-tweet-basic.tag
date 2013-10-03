<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core"%><%
%><%@ attribute name="tweet" required="true" type="in.fount.model.Tweet"%><%

%>created_at: "${tweet.created_at}",<%
%>from_user: "${tweet.from_user}",<%
%>from_user_id: ${tweet.from_user_id},<%
%>from_user_id_str: "${tweet.from_user_id_str}",<%
%>from_user_name: "${tweet.from_user_name}",<%
%>health: ${tweet.health},<%

//TODO: need to look at this and see which is better
%>geo: {
    coordinates: [<c:if test="${not empty tweet.geo.coordinates}"><%
        %>${tweet.geo.coordinates[0]}, ${tweet.geo.coordinates[1]}<%
        %></c:if>]<%
%>},<%

%>id: ${tweet.id},<%
%>id_str: "${tweet.id_str}",<%
%>profile_image_url: "${tweet.profile_image_url}",<%
%>profile_image_url_https: "${tweet.profile_image_url_https}",<%
%>source: "<%= org.apache.commons.lang.StringEscapeUtils.escapeHtml(tweet.getSource()) %>",<%
%>text: "<%= org.apache.commons.lang.StringEscapeUtils.escapeJavaScript(tweet.getText()) %>",<%
%>to_user: "${tweet.to_user}",<%
%>to_user_id: ${tweet.to_user_id},<%
%>to_user_id_str: "${tweet.to_user_id_str}",<%
// this call is taxing on our limited calls and the field is never used... 
%>to_user_name: ""
