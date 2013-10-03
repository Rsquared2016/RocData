package in.fount.model;

import org.codehaus.jackson.annotate.JsonIgnore;
import org.ektorp.support.CouchDbDocument;

/**
 * Represents Google place, see <a
 * href="https://developers.google.com/maps/documentation/places/">Google Places
 * API</a>
 */
public class GPlace extends CouchDbDocument {

    private static final long serialVersionUID = 9069298121782594443L;

    private String name;

    private GeoLocation geo_location;

    @JsonIgnore
    private String[] types;

    @JsonIgnore
    private String rating;

    @JsonIgnore
    private String reference;

    @JsonIgnore
    private String vicinity;

    @JsonIgnore
    private String icon;

    @JsonIgnore
    private String id;

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public GeoLocation getGeo_location() {
        return geo_location;
    }

    public void setGeo_location(GeoLocation geo_location) {
        this.geo_location = geo_location;
    }

}
