package in.fount.service.mobile;

import in.fount.model.mobile.ClassifyRequest;
import in.fount.model.mobile.Feedback;
import in.fount.model.mobile.GeoRequest;
import in.fount.model.mobile.SelfReport;

import java.util.HashMap;
import java.util.Map;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.client.RestTemplate;

/**
 * This service comunicates to the mobile daemon using {@link RestTemplate}. The
 * target database is the <code>m</code> database.
 */
public class TweetMRepository {

    private static final String TWEET_URL_GET_BBOX = "/tweets?left={left}&bottom={bottom}&right={right}&top={top}";

    private static final String LOCATION_PART = "&user_lat={user_lat}&user_lon={user_lon}";

    private static final String TWEET_URL_PARAMS_POST = "/feedback?userID={userID}&feedback={feedback}&tweetID={tweetID}&lat={lat}&lon={lon}";

    private static final String CLASSIFY_URL_POST = "/classify";

    private static final String SELF_REPORT_URL_POST = "/self_report";

    private static final String HEALTH_PART = "&health={health}";

    private static final String HEALTH_ATTRIBUTE = "health";

    private static final String USER_LAT_ATTRIBUTE = "user_lat";

    private static final String USER_LON_ATTRIBUTE = "user_lon";

    private static final String LEFT_ATTRIBUTE = "left";

    private static final String RIGHT_ATTRIBUTE = "right";

    private static final String BOTTOM_ATTRIBUTE = "bottom";

    private static final String TOP_ATTRIBUTE = "top";

    private static Logger log = LoggerFactory.getLogger(TweetMRepository.class);

    private String serverUrl;

    @Autowired
    private RestTemplate restTemplate;

    public GeoRequest getTweets(double left, double bottom, double right,
            double top, Double health, Double user_lat, Double user_lon) {

        log.debug(
                "requesting tweets in bounds [left: {}, right: {}, bottom: {}, top: {}] with health {} and location [lat={}, lng={}]",
                new Object[] { left, bottom, right, top, health, user_lat,
                        user_lon });

        StringBuilder url = new StringBuilder(serverUrl + TWEET_URL_GET_BBOX);
        Map<String, Object> urlVariables = new HashMap<String, Object>();
        urlVariables.put(LEFT_ATTRIBUTE, left);
        urlVariables.put(RIGHT_ATTRIBUTE, right);
        urlVariables.put(BOTTOM_ATTRIBUTE, bottom);
        urlVariables.put(TOP_ATTRIBUTE, top);

        if (health != null) {
            url.append(HEALTH_PART);
            urlVariables.put(HEALTH_ATTRIBUTE, health);
        }

        if (user_lat != null && user_lon != null) {
            url.append(LOCATION_PART);
            urlVariables.put(USER_LAT_ATTRIBUTE, user_lat);
            urlVariables.put(USER_LON_ATTRIBUTE, user_lon);
        }

        GeoRequest radar = restTemplate.getForObject(url.toString(),
                GeoRequest.class, urlVariables);

        log.debug("fetched {} tweets", radar.getNum_docs());

        return radar;
    }

    public ClassifyRequest postTweets(ClassifyRequest tweets) {
        return restTemplate.postForObject(serverUrl + CLASSIFY_URL_POST,
                tweets, ClassifyRequest.class);
    }

    public String postFeedback(Feedback feedback, String id, double lat,
            double lng) {
        return restTemplate.getForObject(serverUrl + TWEET_URL_PARAMS_POST,
                String.class, feedback.getUser_id(), feedback.getRating(), id,
                lat, lng);
    }

    public String postSelfReport(SelfReport selfReport) {
        return restTemplate.postForObject(serverUrl + SELF_REPORT_URL_POST,
                selfReport, String.class);
    }

    // getters & setters

    public void setServerUrl(String serverUrl) {
        this.serverUrl = serverUrl;
    }

}
