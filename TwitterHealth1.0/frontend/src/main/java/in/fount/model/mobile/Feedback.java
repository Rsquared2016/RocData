package in.fount.model.mobile;

import java.io.Serializable;

public class Feedback implements Serializable {

    private static final long serialVersionUID = 1L;

    private int rating;

    private String user_id;

    private String time;

    public int getRating() {
        return rating;
    }

    public void setRating(int rating) {
        this.rating = rating;
    }

    public String getUser_id() {
        return user_id;
    }

    public void setUser_id(String user_id) {
        this.user_id = user_id;
    }

    public String getTime() {
        return time;
    }

    public void setTime(String time) {
        this.time = time;
    }

}
