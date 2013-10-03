package in.fount.util;

import in.fount.model.Geometry;
import in.fount.model.mobile.Tweet;

import java.util.ArrayList;
import java.util.LinkedList;
import java.util.List;

import twitter4j.Status;

public class MobileTweetHelper {

    public static Tweet statusToMobileTweet(Status s) {

        Tweet tweet = new Tweet();

        tweet.setId("" + s.getId());
        tweet.setTwitterId(s.getId());
        tweet.setId_str("" + s.getId());
        tweet.setCreated_at(s.getCreatedAt().toString());
        tweet.setFrom_user(s.getUser().getScreenName());
        tweet.setFrom_user_id(s.getUser().getId());
        tweet.setFrom_user_id_str("" + s.getUser().getId());
        tweet.setFrom_user_name(s.getUser().getName());
        Geometry geo = new Geometry();
        ArrayList<Double> coords = new ArrayList<Double>();
        if (s.getGeoLocation() != null) {
            coords.add(s.getGeoLocation().getLatitude());
            coords.add(s.getGeoLocation().getLongitude());
        }
        geo.setCoordinates(coords);
        tweet.setGeo(geo);
        tweet.setLive_classified(false);
        tweet.setProfile_image_url(s.getUser().getProfileImageURL().toString());
        tweet.setProfile_image_url_https(s.getUser().getProfileImageURL()
                .toString());
        tweet.setSource(s.getSource());
        tweet.setText(s.getText());
        tweet.setTo_user(s.getInReplyToScreenName());
        tweet.setTo_user_id(s.getInReplyToUserId());
        tweet.setTo_user_id_str("" + s.getInReplyToUserId());
        // no straightforward way of getting their actual name here
        tweet.setTo_user_name(s.getInReplyToScreenName());

        return tweet;
    }

    public static List<Tweet> statusesToMobileTweets(List<Status> statuses) {
        List<Tweet> result = new LinkedList<Tweet>();

        for (Status status : statuses)
            result.add(statusToMobileTweet(status));

        return result;
    }

}
