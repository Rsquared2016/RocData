package in.fount.model;

import java.util.HashMap;

import org.codehaus.jackson.annotate.JsonIgnore;
import org.ektorp.support.CouchDbDocument;
import org.ektorp.support.TypeDiscriminator;

public class Tweet extends CouchDbDocument {

    private static final long serialVersionUID = 1L;

    @TypeDiscriminator
    private double health;
    private double lat;
    private double lon;
    private Geometry geo;
    private String location;

    private String created_at;
    private String source;
    private String text;
    @JsonIgnore
    private String id;
    @JsonIgnore
    private String[] taxonomy;
    @JsonIgnore
    private String place;
    private String id_str;
    private String iso_language_code;
    private String in_reply_to_status_id;
    private String in_reply_to_status_id_str;

    private String from_user;
    private String from_user_id;
    private String from_user_id_str;
    private String from_user_name;

    private String to_user;
    private String to_user_id;
    private String to_user_id_str;
    private String to_user_name;

    private String profile_image_url;
    private String profile_image_url_https;

    @SuppressWarnings({ "rawtypes" })
    @JsonIgnore
    private HashMap metadata;

    // Getters
    public double getHealth() {
        return health;
    }

    public double getLat() {
        return lat;
    }

    public double getLon() {
        return lon;
    }

    public Geometry getGeo() {
        return geo;
    }

    public String getLocation() {
        return location;
    }

    public String getCreated_at() {
        return created_at;
    }

    public String getSource() {
        return source;
    }

    public String getText() {
        return text;
    }

    public String getFrom_user() {
        return from_user;
    }

    public String getFrom_user_id() {
        return from_user_id;
    }

    public String getFrom_user_id_str() {
        return from_user_id_str;
    }

    public String getFrom_user_name() {
        return from_user_name;
    }

    public String getTo_user() {
        return to_user;
    }

    public String getTo_user_id() {
        return to_user_id;
    }

    public String getTo_user_id_str() {
        return to_user_id_str;
    }

    public String getTo_user_name() {
        return to_user_name;
    }

    public String getId() {
        return id;
    }

    public String getId_str() {
        return id_str;
    }

    public String getIso_language_code() {
        return iso_language_code;
    }

    public String getIn_reply_to_status_id() {
        return in_reply_to_status_id;
    }

    public String getIn_reply_to_status_id_str() {
        return in_reply_to_status_id_str;
    }

    public String getProfile_image_url() {
        return profile_image_url;
    }

    public String getProfile_image_url_https() {
        return profile_image_url_https;
    }

    public String[] getTaxonomy() {
        return taxonomy;
    }

    // Setters
    public void setHealth(double s) {
        health = s;
    }

    public void setLat(double s) {
        lat = s;
    }

    public void setLon(double s) {
        lon = s;
    }

    public void setGeo(Geometry s) {
        geo = s;
    }

    public void setLocation(String s) {
        location = s;
    }

    public void setCreated_at(String s) {
        created_at = s;
    }

    public void setSource(String s) {
        source = s;
    }

    public void setText(String s) {
        text = s;
    }

    public void setFrom_user(String s) {
        from_user = s;
    }

    public void setFrom_user_id(String s) {
        from_user_id = s;
    }

    public void setFrom_user_id_str(String s) {
        from_user_id_str = s;
    }

    public void setFrom_user_name(String s) {
        from_user_name = s;
    }

    public void setTo_user(String s) {
        to_user = s;
    }

    public void setTo_user_id(String s) {
        to_user_id = s;
    }

    public void setTo_user_id_str(String s) {
        to_user_id_str = s;
    }

    public void setTo_user_name(String s) {
        to_user_name = s;
    }

    public void setId(String s) {
        id = s;
    }

    public void setId_str(String s) {
        id_str = s;
    }

    public void setIso_language_code(String s) {
        iso_language_code = s;
    }

    public void setIn_reply_to_status_id(String s) {
        in_reply_to_status_id = s;
    }

    public void setIn_reply_to_status_id_str(String s) {
        in_reply_to_status_id_str = s;
    }

    public void setProfile_image_url(String s) {
        profile_image_url = s;
    }

    public void setProfile_image_url_https(String s) {
        profile_image_url_https = s;
    }

    public void setTaxonomy(String[] taxonomy) {
        this.taxonomy = taxonomy;
    }

    public void setStatus(twitter4j.Status s) {

    }

}
