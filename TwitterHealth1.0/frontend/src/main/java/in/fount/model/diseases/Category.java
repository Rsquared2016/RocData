package in.fount.model.diseases;

import java.util.ArrayList;
import java.util.List;

public class Category {

    private String name;

    private List<LatLng> tweets = new ArrayList<LatLng>();

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public List<LatLng> getTweets() {
        return tweets;
    }

    @Override
    public String toString() {
        return "[Category name: " + name + "]";
    }

}
