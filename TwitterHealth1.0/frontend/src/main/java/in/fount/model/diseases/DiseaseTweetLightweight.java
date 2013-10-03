package in.fount.model.diseases;

import in.fount.model.Geometry;

import org.codehaus.jackson.annotate.JsonIgnore;
import org.ektorp.support.CouchDbDocument;

public class DiseaseTweetLightweight extends CouchDbDocument {

    private static final long serialVersionUID = 1L;

    private Taxonomy taxonomy;

    private Geometry geo;

    private String created_at;

    private String from_user;
    @JsonIgnore
    private String from_user_id;
    @JsonIgnore
    private String from_user_id_str;

    @JsonIgnore
    private String from_user_name;

    @JsonIgnore
    private String id;

    private String id_str;

    @JsonIgnore
    private String iso_language_code;

    @JsonIgnore
    private String location;

    @JsonIgnore
    private String metadata;

    @JsonIgnore
    private String profile_image_url;

    @JsonIgnore
    private String profile_image_url_https;

    @JsonIgnore
    private String source;

    private String text;

    @JsonIgnore
    private String to_user;

    @JsonIgnore
    private String to_user_id;

    @JsonIgnore
    private String to_user_id_str;

    @JsonIgnore
    private String to_user_name;

    @JsonIgnore
    private String in_reply_to_status_id;

    @JsonIgnore
    private String in_reply_to_status_id_str;

    @JsonIgnore
    private String in_reply_to_status_id_name;

    @JsonIgnore
    private double lat;

    @JsonIgnore
    private double lon;

    @JsonIgnore
    private String health;

    public Taxonomy getTaxonomy() {
        return taxonomy;
    }

    public void setTaxonomy(Taxonomy taxonomy) {
        this.taxonomy = taxonomy;
    }

    public Geometry getGeo() {
        return geo;
    }

    public void setGeo(Geometry geo) {
        this.geo = geo;
    }

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

    public String getId_str() {
        return id_str;
    }

    public void setId_str(String id_str) {
        this.id_str = id_str;
    }

    public String getText() {
        return text;
    }

    public void setText(String text) {
        this.text = text;
    }

    @Override
    public boolean equals(Object other) {

        if (other instanceof DiseaseTweetLightweight)
            return getId().equals(((DiseaseTweetLightweight) other).getId());

        return false;
    }

    @Override
    public int hashCode() {
        int hash = 7;
        hash = 31 * hash + (getId() == null ? 0 : getId().hashCode());
        return hash;
    }

    @Override
    public String toString() {

        StringBuilder sb = new StringBuilder("[Tweet created_at: ");
        sb.append(created_at);
        if (taxonomy != null) {
            sb.append(", disease: ");
            sb.append(taxonomy.getDisease());
            sb.append(", terms: ");
            sb.append(taxonomy.getTerms());
        }

        if (geo != null) {
            sb.append(", geo: [lat: ");
            sb.append(geo.getCoordinates().get(0));
            sb.append(", lng: ");
            sb.append(geo.getCoordinates().get(1));
            sb.append("]");
        }
        sb.append("]");

        return sb.toString();
    }
}
