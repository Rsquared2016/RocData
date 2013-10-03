package in.fount.model.mobile;

import java.util.List;

import org.ektorp.support.CouchDbDocument;

public class GeoRequest extends CouchDbDocument {

    private static final long serialVersionUID = 1L;

    private List<Tweet> tweets;
    private List<SelfReport> self_reports;
    private double health_risk = 0.0;
    private int num_docs;

    public List<Tweet> getTweets() {
        return tweets;
    }

    public void setTweets(List<Tweet> tweets) {
        this.tweets = tweets;
    }

    public List<SelfReport> getSelf_reports() {
        return self_reports;
    }

    public void setSelf_reports(List<SelfReport> self_reports) {
        this.self_reports = self_reports;
    }

    public double getHealth_risk() {
        return health_risk;
    }

    public void setHealth_risk(double health_risk) {
        this.health_risk = health_risk;
    }

    public int getNum_docs() {
        return num_docs;
    }

    public void setNum_docs(int num_docs) {
        this.num_docs = num_docs;
    }

}
