package in.fount.model;

import org.ektorp.support.CouchDbDocument;
import org.ektorp.support.TypeDiscriminator;

public class Status extends CouchDbDocument {

    private static final long serialVersionUID = 1L;

    @TypeDiscriminator
    private twitter4j.Status status;

    public twitter4j.Status getStatus() {
        return status;
    }

    public void setStatus(twitter4j.Status status) {
        this.status = status;
    }

}
