package in.fount.model.mobile;

import in.fount.model.GeoLocation;

import org.ektorp.support.CouchDbDocument;

public class Point extends CouchDbDocument {

    private static final long serialVersionUID = 1L;

    private GeoLocation location;
    private String created_at;
    private double health;

    public GeoLocation getLocation() {
        return location;
    }

    public void setLocation(GeoLocation location) {
        this.location = location;
    }

    public String getCreated_at() {
        return created_at;
    }

    public void setCreated_at(String created_at) {
        this.created_at = created_at;
    }

    public double getHealth() {
        return health;
    }

    public void setHealth(double health) {
        this.health = health;
    }

}
