package in.fount.model.mobile;

import in.fount.model.Geometry;

import java.util.List;

import org.codehaus.jackson.annotate.JsonIgnore;
import org.codehaus.jackson.annotate.JsonProperty;
import org.ektorp.support.CouchDbDocument;

public class Tweet extends CouchDbDocument {

    private static final long serialVersionUID = 1L;

    private String created_at;
    private String from_user;
    private long from_user_id;
    private String from_user_id_str;
    private String from_user_name;
    private Geometry geo;
    private double health;
    private long id;
    private String id_str;
    @JsonIgnore
    private String iso_language_code;
    private boolean live_classified;
    @JsonIgnore
    private String location;
    @JsonIgnore
    private Object metadata;
    @JsonIgnore
    private long in_reply_to_status_id;
    @JsonIgnore
    private String in_reply_to_status_id_str;
    private String profile_image_url;
    private String profile_image_url_https;
    private String source;
    private String text;
    private String to_user;
    private long to_user_id;
    private String to_user_id_str;
    private String to_user_name;
    private List<Feedback> feedback;

    public String getCreated_at() {
        return created_at;
    }

    public void setCreated_at(String created_at) {
        this.created_at = created_at;
    }

    public String getFrom_user() {
        return from_user;
    }

    public void setFrom_user(String from_user) {
        this.from_user = from_user;
    }

    public long getFrom_user_id() {
        return from_user_id;
    }

    public void setFrom_user_id(long from_user_id) {
        this.from_user_id = from_user_id;
    }

    public String getFrom_user_id_str() {
        return from_user_id_str;
    }

    public void setFrom_user_id_str(String from_user_id_str) {
        this.from_user_id_str = from_user_id_str;
    }

    public String getFrom_user_name() {
        return from_user_name;
    }

    public void setFrom_user_name(String from_user_name) {
        this.from_user_name = from_user_name;
    }

    public Geometry getGeo() {
        return geo;
    }

    public void setGeo(Geometry geo) {
        this.geo = geo;
    }

    public double getHealth() {
        return health;
    }

    public void setHealth(double health) {
        this.health = health;
    }

    public String getId_str() {
        return id_str;
    }

    public void setId_str(String id_str) {
        this.id_str = id_str;
    }

    public String getIso_language_code() {
        return iso_language_code;
    }

    public void setIso_language_code(String iso_language_code) {
        this.iso_language_code = iso_language_code;
    }

    public String getLocation() {
        return location;
    }

    public void setLocation(String location) {
        this.location = location;
    }

    public Object getMetadata() {
        return metadata;
    }

    public void setMetadata(Object metadata) {
        this.metadata = metadata;
    }

    public String getProfile_image_url() {
        return profile_image_url;
    }

    public void setProfile_image_url(String profile_image_url) {
        this.profile_image_url = profile_image_url;
    }

    public String getProfile_image_url_https() {
        return profile_image_url_https;
    }

    public void setProfile_image_url_https(String profile_image_url_https) {
        this.profile_image_url_https = profile_image_url_https;
    }

    public String getSource() {
        return source;
    }

    public void setSource(String source) {
        this.source = source;
    }

    public String getText() {
        return text;
    }

    public void setText(String text) {
        this.text = text;
    }

    public String getTo_user() {
        return to_user;
    }

    public void setTo_user(String to_user) {
        this.to_user = to_user;
    }

    public long getTo_user_id() {
        return to_user_id;
    }

    public void setTo_user_id(long to_user_id) {
        this.to_user_id = to_user_id;
    }

    public String getTo_user_id_str() {
        return to_user_id_str;
    }

    public void setTo_user_id_str(String to_user_id_str) {
        this.to_user_id_str = to_user_id_str;
    }

    public String getTo_user_name() {
        return to_user_name;
    }

    public void setTo_user_name(String to_user_name) {
        this.to_user_name = to_user_name;
    }

    public List<Feedback> getFeedback() {
        return feedback;
    }

    public void setFeedback(List<Feedback> feedback) {
        this.feedback = feedback;
    }

    @JsonProperty("id")
    public long getTwitterId() {
        return id;
    }

    @JsonProperty("id")
    public void setTwitterId(long id) {
        this.id = id;
    }

    public boolean isLive_classified() {
        return live_classified;
    }

    public void setLive_classified(boolean live_classified) {
        this.live_classified = live_classified;
    }

}
