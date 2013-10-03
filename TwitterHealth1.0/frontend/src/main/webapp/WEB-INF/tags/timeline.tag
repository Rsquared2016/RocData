<%@ attribute name="tweets" required="false" type="java.util.List" %><%

final String[] months = 
	{"Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"};
final String  userLink = 
	" <a  target=\"_blank\" alt=\"twitter feed for user $2\" href=\"http://twitter.com/$2\" > @$2</a>";
final String hashtagLink = 
	" <a  target=\"_blank\"  alt=\"twitter hashtag search for $2\" href=\"http://twitter.com/#!/search?q=%23$2\"> #$2 </a>";

 final java.util.regex.Pattern auser = java.util.regex.Pattern.compile("(^|\\s|\")@([\\w]+)");
final java.util.regex.Pattern ahashtag = java.util.regex.Pattern.compile("(^|\\s|\")#([\\w]+)");

for (twitter4j.Status status : (java.util.List<twitter4j.Status>)tweets) {
				String tweet = status.getText();

				// --- Prevent stupid follow fridays from showing.
				if(!tweet.toLowerCase().contains("#ff")){
					
					boolean geo = status.getGeoLocation()!=null;
					
					%><div style="background:<%if(geo){%>green<%}else{%>red<%}%>"><a  style="float:left; clear:both;" 
							rel="me nofollow" 
							target="_blank" 
							href="http://twitter.com/<%=status.getUser().getScreenName()%>"
							title="<%=status.getUser().getScreenName()%>'s twitter feed" >
							<img 	class="avatar"  
									alt="<%=status.getUser().getScreenName()%>'s avatar" 
									src="<%=status.getUser().getProfileImageURL()%>"/>
					</a>
					<a	style="float:left;" class="screenname" 
						rel="me nofollow" 
						target="_blank" 
						href="http://twitter.com/<%=status.getUser().getScreenName()%>" 
						title="<%=status.getUser().getScreenName()%>'s twitter feed"> 

						<%=status.getUser().getScreenName()%> </a><br/><%

					// --- linkify
					tweet= auser.matcher(tweet).replaceAll(userLink);
					tweet= ahashtag.matcher(tweet).replaceAll(hashtagLink);

					for(twitter4j.URLEntity u: status.getURLEntities()){
						if(u.getDisplayURL()!=null)
							
							tweet=tweet.replace(
									u.getURL().toString(),
									" <a target=\"_blank\" href=\""+
										u.getURL().toString()+
										"\"  rel=\"nofollow\" > "
										+u.getDisplayURL()+
									"</a>"
									);
						
						else
							tweet=tweet.replace(
									u.getURL().toString(),
									" <a target=\"_blank\" href=\""+
									u.getURL()+
									"\"  rel=\"nofollow\"> "
									+u.getURL()+"</a>");
					}


					%> <span class="tweet-text"> <%=tweet%> </span> <%


					// --- build the time
					%><br/><span class="tweet-time"><%
					Long elapsed = (new java.util.Date()).getTime()-status.getCreatedAt().getTime();
					if(elapsed < 60000) {
						int t=Math.round(elapsed/1000);
						%> <%=t%> second<%
						if(t !=1){%>s<%}
						%> ago<%

					} else if(elapsed < 3600000) {
						int t=Math.round(elapsed/60000);
						%> <%=t%> minute<%
						if(t !=1){%>s<%}
						%> ago<%

					} else if(elapsed < 86400000) {
						int t=Math.round(elapsed/3600000);
						%> <%=t%> hour<%
						if(t !=1){%>s<%}
						%> ago<%
					}
					else{
						%> on <%=months[status.getCreatedAt().getMonth()] %> <%=status.getCreatedAt().getDate()%><%
					}
					%></span><%
					%><%=status.getGeoLocation()%><%
					%></div><%
				}
			}// --- end for loop.
%>