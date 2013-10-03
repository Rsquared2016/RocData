package in.fount.service;

import in.fount.model.Tweet;
import in.fount.util.CalendarUtils;
import in.fount.util.TweetRepositoryHelper;

import java.util.Date;
import java.util.List;

import org.ektorp.ComplexKey;
import org.ektorp.CouchDbConnector;
import org.ektorp.Page;
import org.ektorp.PageRequest;
import org.ektorp.ViewQuery;
import org.ektorp.support.CouchDbRepositorySupport;
import org.ektorp.support.View;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.stereotype.Component;

/**
 * Couchdb repository connector for the <code>all_sick_healthy_rack</code>
 * database.
 */
@Component
public class HealthRepository extends CouchDbRepositorySupport<Tweet> {

    private static final String DESIGN_TWEET = "_design/Tweet";

    private static final String ALL_VIEW = "all";

    private static final String DAYS_VIEW = "days";

    private static final String BY_DAY_VIEW = "by_day";

    @Autowired
    public HealthRepository(
            @Qualifier("all_sick_healthy_rack") CouchDbConnector db) {
        super(Tweet.class, db);
        initStandardDesignDocument();
    }

    @Override
    @View(name = ALL_VIEW, map = "classpath:/couchdb/views/health/all_sick_healthy_rack/all.js")
    public List<Tweet> getAll() {
        ViewQuery q = createQuery(ALL_VIEW).descending(true).includeDocs(true);
        List<Tweet> result = db.queryView(q, Tweet.class);

        logResult(result);

        return result;
    }

    @View(name = ALL_VIEW, map = "classpath:/couchdb/views/health/all_sick_healthy_rack/all.js")
    public Page<Tweet> getAll(PageRequest pr) {
        ViewQuery q = createQuery(ALL_VIEW).descending(true).includeDocs(true)
                .staleOk(true);
        Page<Tweet> result = db.queryForPage(q, pr, Tweet.class);

        logResult(result);

        return result;
    }

    /**
     * @return list of unique days from the database
     */
    @View(name = DAYS_VIEW, map = "classpath:/couchdb/views/health/all_sick_healthy_rack/days_map.js", reduce = "classpath:/couchdb/views/health/all_sick_healthy_rack/days_reduce.js")
    public List<Date> getAvailableDays() {
        List<Date> result = TweetRepositoryHelper.getAvailableDays(db,
                DESIGN_TWEET, DAYS_VIEW);

        logDaysResult(result);

        return result;
    }

    @View(name = BY_DAY_VIEW, map = "classpath:/couchdb/views/health/all_sick_healthy_rack/by_day_map.js")
    public List<Tweet> getTweetsByDay(Date date) {
        int year, month, day;
        year = CalendarUtils.getYear(date);
        month = CalendarUtils.getMonth(date);
        day = CalendarUtils.getDay(date);

        ComplexKey key = ComplexKey.of(year, month, day);

        ViewQuery query = new ViewQuery().designDocId(DESIGN_TWEET)
                .viewName(BY_DAY_VIEW).key(key);

        List<Tweet> result = db.queryView(query, Tweet.class);

        logResult(result);

        return result;
    }

    private void logResult(List<Tweet> result) {
        log.debug("fetched {} health-tagged tweets ", result.size());
        if (log.isTraceEnabled()) {
            for (Tweet tweet : result) {
                log.trace("tweet: {}", tweet);
            }
        }
    }

    private void logResult(Page<Tweet> result) {
        log.debug("fetched {} health-tagged tweets ", result.size());
        if (log.isTraceEnabled()) {
            for (Tweet tweet : result) {
                log.trace("tweet: {}", tweet);
            }
        }
    }

    private void logDaysResult(List<Date> result) {
        log.debug("found {} available days", result.size());
        if (log.isTraceEnabled()) {
            for (Date day : result) {
                log.trace("day: {}", day);
            }
        }
    }

}
