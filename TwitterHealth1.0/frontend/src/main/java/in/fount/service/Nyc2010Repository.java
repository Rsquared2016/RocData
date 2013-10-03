package in.fount.service;

import in.fount.model.Tweet;
import in.fount.util.CalendarUtils;

import java.util.ArrayList;
import java.util.Date;
import java.util.List;

import org.codehaus.jackson.JsonNode;
import org.ektorp.ComplexKey;
import org.ektorp.CouchDbConnector;
import org.ektorp.Page;
import org.ektorp.PageRequest;
import org.ektorp.ViewQuery;
import org.ektorp.ViewResult;
import org.ektorp.ViewResult.Row;
import org.ektorp.changes.ChangesCommand;
import org.ektorp.changes.DocumentChange;
import org.ektorp.support.CouchDbRepositorySupport;
import org.ektorp.support.GenerateView;
import org.ektorp.support.View;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.stereotype.Component;

@Component
public class Nyc2010Repository extends CouchDbRepositorySupport<Tweet> {

    private static final String DESIGN_TWEET = "_design/Tweet";

    private static final String ALL_VIEW = "all";

    private static final String DAYS_VIEW = "days";

    private static final String BY_DAY_VIEW = "by_day";

    @Autowired
    public Nyc2010Repository(@Qualifier("nyc_one_month") CouchDbConnector db) {
        super(Tweet.class, db);
        initStandardDesignDocument();
    }

    @GenerateView
    @Override
    public List<Tweet> getAll() {
        ViewQuery q = createQuery(ALL_VIEW).descending(true).includeDocs(true)
                .limit(5000);
        return db.queryView(q, Tweet.class);
    }

    public Page<Tweet> getAll(PageRequest pr) {
        ViewQuery q = createQuery(ALL_VIEW).descending(true).includeDocs(true)
                .staleOk(true);
        return db.queryForPage(q, pr, Tweet.class);
    }

    /**
     * @return list of unique days from the database
     */
    @View(name = DAYS_VIEW, map = "classpath:/couchdb/views/pollution/nyc_one_month/days_map.js", reduce = "classpath:/couchdb/views/pollution/nyc_one_month/days_reduce.js")
    public List<Date> getAvailableDays() {
        ViewQuery query = new ViewQuery().designDocId(DESIGN_TWEET)
                .viewName(DAYS_VIEW).group(true);
        ViewResult result = db.queryView(query);

        List<Date> list = new ArrayList<Date>();

        int year, month, day;
        for (Row row : result) {
            JsonNode node = row.getKeyAsNode();
            year = node.get(0).getIntValue();
            month = node.get(1).getIntValue();
            day = node.get(2).getIntValue();
            log.debug("found date: {}, {}, {}",
                    new Object[] { year, month, day });
            list.add(CalendarUtils.newDate(year, month, day));
        }

        return list;
    }

    @View(name = BY_DAY_VIEW, map = "classpath:/couchdb/views/pollution/nyc_one_month/by_day_map.js", reduce = "classpath:/couchdb/views/pollution/nyc_one_month/by_day_reduce.js")
    public List<Tweet> getTweetsByDay(Date date) {
        int year, month, day;
        year = CalendarUtils.getYear(date);
        month = CalendarUtils.getMonth(date);
        day = CalendarUtils.getDay(date);

        ComplexKey key = ComplexKey.of(year, month, day);

        ViewQuery query = new ViewQuery().designDocId(DESIGN_TWEET)
                .viewName(BY_DAY_VIEW).reduce(false).includeDocs(true).key(key);

        return db.queryView(query, Tweet.class);
    }

    public List<DocumentChange> getChanges(ChangesCommand cmd) {
        return db.changes(cmd);
    }

    public long getUpdateSeq() {
        return db.getDbInfo().getUpdateSeq();
    }
}
