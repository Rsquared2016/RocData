package in.fount.service;

import in.fount.model.Status;

import java.util.List;

import org.ektorp.CouchDbConnector;
import org.ektorp.Page;
import org.ektorp.PageRequest;
import org.ektorp.ViewQuery;
import org.ektorp.support.CouchDbRepositorySupport;
import org.ektorp.support.GenerateView;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.stereotype.Component;

/**
 * Couchdb repository connector for the <code>oauth</code> database.
 */
@Component
public class OauthRepository extends CouchDbRepositorySupport<Status> {

    private static final String ALL_VIEW = "all";

    @Autowired
    public OauthRepository(@Qualifier("oauth") CouchDbConnector db) {
        super(Status.class, db);
        initStandardDesignDocument();
    }

    @GenerateView
    @Override
    public List<Status> getAll() {
        ViewQuery q = createQuery(ALL_VIEW).descending(true).includeDocs(true);
        List<Status> result = db.queryView(q, Status.class);

        logResult(result);

        return result;
    }

    public Page<Status> getAll(PageRequest pr) {
        ViewQuery q = createQuery(ALL_VIEW).descending(true).includeDocs(true)
                .staleOk(true);
        Page<Status> result = db.queryForPage(q, pr, Status.class);

        logResult(result);

        return result;
    }

    private void logResult(List<Status> result) {
        log.debug("fetched {} statuses ", result.size());
        if (log.isTraceEnabled()) {
            for (Status status : result) {
                log.trace("tweet: {}", status);
            }
        }
    }

    private void logResult(Page<Status> result) {
        log.debug("fetched {} statuses ", result.size());
        if (log.isTraceEnabled()) {
            for (Status status : result) {
                log.trace("tweet: {}", status);
            }
        }
    }

}
