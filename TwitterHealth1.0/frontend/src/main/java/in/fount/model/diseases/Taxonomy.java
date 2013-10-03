package in.fount.model.diseases;

import org.ektorp.support.CouchDbDocument;

public class Taxonomy extends CouchDbDocument {

    private static final long serialVersionUID = 1L;

    private String terms;

    private String disease;

    public String getTerms() {
        return terms;
    }

    public void setTerms(String terms) {
        this.terms = terms;
    }

    public String getDisease() {
        return disease;
    }

    public void setDisease(String disease) {
        this.disease = disease;
    }

}
