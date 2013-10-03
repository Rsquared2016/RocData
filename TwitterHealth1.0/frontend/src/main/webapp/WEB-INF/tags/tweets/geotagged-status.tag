<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core"%><%
%><%@ attribute name="tweet" required="true" type="twitter4j.Status"%><%

%>created_at: "${tweet.createdAt}",<%
%>feedback: [],<%
%>from_user: "${tweet.user.screenName}",<%
%>from_user_id: ${tweet.user.id},<%
%>from_user_id_str: "${tweet.user.id}",<%
%>from_user_name: "${tweet.user.name}",<%
%>health: 0.0,<%

//TODO: need to look at this and see which is better
%>geo: {
    coordinates: [
        <c:if test="${not empty tweet.geoLocation}">
        ${tweet.geoLocation.latitude},
        ${tweet.geoLocation.longitude}
        </c:if>
    ]
},<%

%>id: ${tweet.id},<%
%>id_str: "${tweet.id}",<%
%>profile_image_url: "${tweet.user.profileImageURL}",<%
%>profile_image_url_https: "${tweet.user.profileImageUrlHttps}",<%
%>source: "<%= org.apache.commons.lang.StringEscapeUtils.escapeHtml(tweet.getSource()) %>",<%
%>to_user: "${tweet.inReplyToScreenName}",<%
%>to_user_id: ${tweet.inReplyToUserId},<%
%>to_user_id_str: "${tweet.inReplyToUserId}",<%
%>text: "<%= org.apache.commons.lang.StringEscapeUtils.escapeJavaScript(tweet.getText()) %>",<%

// this call is taxing on our limited calls and the field is never used... 
%>to_user_name: ""
