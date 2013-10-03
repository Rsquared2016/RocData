package in.fount.model.mobile;

import java.util.List;

import org.ektorp.support.CouchDbDocument;

public class User extends CouchDbDocument {

    private static final long serialVersionUID = 1L;

    private List<Point> points;

    public List<Point> getPoints() {
        return points;
    }

    public void setPoints(List<Point> points) {
        this.points = points;
    }

}
