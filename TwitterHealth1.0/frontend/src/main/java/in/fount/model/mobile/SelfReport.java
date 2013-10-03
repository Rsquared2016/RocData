package in.fount.model.mobile;

import java.util.List;

import in.fount.model.Geometry;

import org.ektorp.support.CouchDbDocument;

public class SelfReport extends CouchDbDocument {

    private static final long serialVersionUID = 1L;

    private Geometry geo;
    private Double health;
    private List<String> symptoms;
    private String twitter_id;
    private String user_id;
    private String created_at;

    public Geometry getGeo() {
        return geo;
    }

    public void setGeo(Geometry geo) {
        this.geo = geo;
    }

    public Double getHealth() {
        return health;
    }

    public void setHealth(Double health) {
        this.health = health;
    }

    public List<String> getSymptoms() {
        return symptoms;
    }

    public void setSymptoms(List<String> symptoms) {
        this.symptoms = symptoms;
    }

    public String getTwitter_id() {
        return twitter_id;
    }

    public void setTwitter_id(String twitter_id) {
        this.twitter_id = twitter_id;
    }

    public String getUser_id() {
        return user_id;
    }

    public void setUser_id(String user_id) {
        this.user_id = user_id;
    }

    public String getCreated_at() {
        return created_at;
    }

    public void setCreated_at(String created_at) {
        this.created_at = created_at;
    }

}
