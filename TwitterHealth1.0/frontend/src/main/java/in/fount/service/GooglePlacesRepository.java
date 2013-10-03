package in.fount.service;

import java.util.List;

import org.ektorp.CouchDbConnector;
import org.ektorp.ViewQuery;
import org.ektorp.support.CouchDbRepositorySupport;

import in.fount.model.GPlace;

public class GooglePlacesRepository extends CouchDbRepositorySupport<GPlace> {

    public GooglePlacesRepository(Class<GPlace> type, CouchDbConnector db) {
        super(type, db);
        initStandardDesignDocument();
    }

    @Override
    public List<GPlace> getAll() {
        ViewQuery q = createQuery("all").includeDocs(true);
        return db.queryView(q, GPlace.class);
    }

}
