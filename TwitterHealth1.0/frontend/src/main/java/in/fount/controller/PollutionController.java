package in.fount.controller;

import static in.fount.util.CalendarUtils.formatDateSlash;
import static in.fount.util.CalendarUtils.parseTweetDate;
import in.fount.model.Tweet;
import in.fount.service.Nyc2010Repository;
import in.fount.util.CityRepoHelper;

import java.util.ArrayList;
import java.util.Collections;
import java.util.Date;
import java.util.HashMap;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;

import org.ektorp.Options;
import org.ektorp.changes.ChangesCommand;
import org.ektorp.changes.DocumentChange;
import org.ektorp.support.CouchDbRepositorySupport;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.format.annotation.DateTimeFormat;
import org.springframework.format.annotation.DateTimeFormat.ISO;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseBody;
import org.springframework.web.servlet.ModelAndView;

@Controller
public class PollutionController {

    private static final String TITLE = "TwitterHealth";

    private static final String NYC = "nyc";

    @Autowired
    private Nyc2010Repository nycRepo;

    @RequestMapping(value = "/pollution", method = RequestMethod.GET)
    public ModelAndView viewDev0Page() {
        ModelAndView view = new ModelAndView("pollution");

        view.addObject("title", TITLE);
        view.addObject("api", "pollution");
        view.addObject("defaultCity", NYC);

        return view;
    }

    @SuppressWarnings("unchecked")
    @RequestMapping(value = "/pollution/data/{city}", method = RequestMethod.GET)
    public @ResponseBody
    Map<String, Object> getDataSetForDev0(
            @PathVariable String city,
            @RequestParam(value = "day", required = false) @DateTimeFormat(iso = ISO.DATE) Date day) {
        // we haven't heard of this city; return empty object
        if (!CityRepoHelper.isValidCity(city)) {
            return Collections.EMPTY_MAP;
        }
        Map<String, Object> pageData = new HashMap<String, Object>();
        Date date = day != null ? day : null;
        // get all tweets and available days
        List<Tweet> tweets = null;
        if (city.equals(NYC)) {
            tweets = date != null ? nycRepo.getTweetsByDay(date) : nycRepo
                    .getAll();
            pageData.put("updateSequence", nycRepo.getUpdateSeq());
        }
        // create tweet lists
        if (date != null)
            pageData.put("tweets", tweets);
        else {
            Map<String, List<Tweet>> tweetsByDay = new HashMap<String, List<Tweet>>();
            pageData.put("tweets", tweetsByDay);
            // add tweets according to their dates
            for (Tweet tweet : tweets) {
                Date tweetDate = parseTweetDate(tweet.getCreated_at());
                String dateStr = formatDateSlash(tweetDate);
                if (tweetsByDay.get(dateStr) == null)
                    tweetsByDay.put(dateStr, new LinkedList<Tweet>());
                tweetsByDay.get(dateStr).add(tweet);
            }
        }

        return pageData;
    }

    @SuppressWarnings("unchecked")
    @RequestMapping(value = "/pollution/changes/{city}", method = RequestMethod.GET)
    public @ResponseBody
    Map<String, Object> getChangesSetForDev0(@PathVariable String city,
            @RequestParam(value = "since", required = false) String since) {
        // we haven't heard of this city; return empty object
        if (!CityRepoHelper.isValidCity(city)) {
            return Collections.EMPTY_MAP;
        }
        // get proper elements for request
        String sn = since != null ? since : "0";
        Map<String, Object> pageData = new HashMap<String, Object>();
        CouchDbRepositorySupport<Tweet> selectedRepo = nycRepo;
        List<DocumentChange> changes = new ArrayList<DocumentChange>();
        ChangesCommand req = new ChangesCommand.Builder().since(sn)
                .filter("Tweet/tagged").build();
        if (city.equals(NYC)) {
            selectedRepo = nycRepo;
            pageData.put("updateSequence", nycRepo.getUpdateSeq());
            changes.addAll(nycRepo.getChanges(req));
        }
        List<Tweet> freshTweets = new LinkedList<Tweet>();
        pageData.put("tweets", freshTweets);
        // get every changed tweet
        for (DocumentChange change : changes) {
            // Tweet fresh = selectedRepo.get(change.getId(),
            // change.getRevision());
            Tweet fresh = selectedRepo.get(change.getId(),
                    new Options().revision(change.getRevision()));
            freshTweets.add(fresh);
        }

        return pageData;
    }
}
