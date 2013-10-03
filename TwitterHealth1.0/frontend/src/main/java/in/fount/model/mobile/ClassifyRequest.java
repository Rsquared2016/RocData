package in.fount.model.mobile;

import java.io.Serializable;
import java.util.List;

public class ClassifyRequest implements Serializable {

    private static final long serialVersionUID = 1L;

    private List<Tweet> tweets;

    public List<Tweet> getTweets() {
        return tweets;
    }

    public void setTweets(List<Tweet> tweets) {
        this.tweets = tweets;
    }

}
