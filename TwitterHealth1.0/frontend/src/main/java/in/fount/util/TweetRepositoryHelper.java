package in.fount.util;

import java.util.ArrayList;
import java.util.Date;
import java.util.List;

import org.codehaus.jackson.JsonNode;
import org.ektorp.CouchDbConnector;
import org.ektorp.ViewQuery;
import org.ektorp.ViewResult;
import org.ektorp.ViewResult.Row;
import org.joda.time.LocalDate;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class TweetRepositoryHelper {

    private static Logger log = LoggerFactory
            .getLogger(TweetRepositoryHelper.class);

    public static List<Date> getAvailableDays(CouchDbConnector db,
            String designDocId, String viewName) {
        ViewQuery query = new ViewQuery().designDocId(designDocId)
                .viewName(viewName).group(true);
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

    public static List<LocalDate> getAvailableLocalDays(CouchDbConnector db,
            String designDocId, String viewName) {
        ViewQuery query = new ViewQuery().designDocId(designDocId)
                .viewName(viewName).group(true);
        ViewResult result = db.queryView(query);

        List<LocalDate> list = new ArrayList<LocalDate>();

        int year, month, day;
        for (Row row : result) {
            JsonNode node = row.getKeyAsNode();
            year = node.get(0).getIntValue();
            month = node.get(1).getIntValue();
            day = node.get(2).getIntValue();
            log.debug("found date: {}, {}, {}",
                    new Object[] { year, month, day });
            list.add(new LocalDate(year, month, day));
        }

        return list;
    }

}
