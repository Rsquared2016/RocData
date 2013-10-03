package in.fount.controller;

import static in.fount.controller.ControllerHelper.buildPage;
import in.fount.model.mobile.GeoRequest;
import in.fount.model.mobile.Tweet;
import in.fount.service.OauthRepository;
import in.fount.util.MobileTweetHelper;

import java.util.LinkedList;
import java.util.List;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpSession;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.ModelAttribute;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.servlet.ModelAndView;

import twitter4j.IDs;
import twitter4j.Paging;
import twitter4j.Status;
import twitter4j.Twitter;
import twitter4j.TwitterException;
import twitter4j.TwitterFactory;
import twitter4j.User;
import twitter4j.auth.AccessToken;
import twitter4j.auth.RequestToken;

@Controller
public class OauthController {

    private static Logger log = LoggerFactory.getLogger(OauthController.class);

    @Autowired
    private OauthRepository OauthRepo;

    @Autowired
    private TwitterFactory twitterFactory;

    @ModelAttribute("twitterFactory")
    public TwitterFactory getTwitterFactory() {
        return twitterFactory;
    }

    @RequestMapping(value = "/oauth", method = RequestMethod.GET)
    public ModelAndView goToOauth() {
        return buildPage("Connecting your health", "oauth/oauth.jsp");
    }

    @RequestMapping(value = "/oauth/twitter/{page}", method = RequestMethod.GET)
    public ModelAndView goToTwitterOauth(@PathVariable String page,
            HttpSession session, HttpServletRequest request) {

        // --- Oauth Specific Stuff:
        User person = null;
        List<Status> statuses = new LinkedList<Status>();
        List<Tweet> tweets = new LinkedList<Tweet>();

        try {
            // handling rate limits cleanly
            Twitter twitter = twitterFactory.getInstance();

            if (session.getAttribute("accessToken") == null) {
                RequestToken requestToken = (RequestToken) session
                        .getAttribute("token");
                session.removeAttribute("token");
                // TODO martin to andrew: still needed?
                // session.removeAttribute("token");
                // BufferedReader br = new BufferedReader(new InputStreamReader(
                // System.in));

                // --- retrieve bits
                String pin = request.getParameter("oauth_verifier");

                // --- check consumer token & secret
                AccessToken accessToken = twitter.getOAuthAccessToken(
                        requestToken, pin);
                session.setAttribute("accessToken", accessToken);
            }

            twitter = twitterFactory.getInstance((AccessToken) session
                    .getAttribute("accessToken"));
            twitter.addRateLimitStatusListener(new LoggingRateLimitHandler());

            // --- grab this person's timeline
            // --- (I can't express how stupid the following line is)
            person = twitter.showUser(twitter.getId());

            IDs followedUsers = twitter.getFriendsIDs(-1);
            Paging paging = new Paging(1, 5);
            int i = 0;

            // --- get timelines of friends
            // --- (we only need one for loop for this)
            for (long id : followedUsers.getIDs()) {
                log.info("Adding {}", id);
                List<Status> results = twitter.getUserTimeline(id, paging);
                statuses.addAll(results);
                log.info("[{}] added", results.size());
                i++;
                if (i >= 100)
                    break;
            }
        } catch (TwitterException e) {
            // TODO martin to andrew: DON'T SWALLOW EXCEPTIONS UNLESS ABSOLUTELY
            // INEVITABLE!
            log.error(e.getMessage(), e);
        }

        // --- Convert statuses pulled into tweets
        tweets.addAll(MobileTweetHelper.statusesToMobileTweets(statuses));

        GeoRequest toPage = new GeoRequest();
        toPage.setTweets(tweets);
        toPage.setHealth_risk(0.0);
        toPage.setNum_docs(tweets.size());
        log.info("Bootstrapping {} tweets to the page.", tweets.size());

        // --- end Oauth Specific stuff ------------------^

        // ----- Build Page to Return --------------------
        ModelAndView toReturn = buildPage("Twitter + Your Health",
                "../oauth/twitter.jsp").addObject("pageName", page).addObject(
                "person", person);

        try {
            if (page.equals("frisco") || page.equals("m")) {
                toReturn.addObject("tweets", toPage.getTweets()).addObject(
                        "health_risk", toPage.getHealth_risk());
            }
        } catch (NullPointerException e) {
            // TODO martin to andrew: NPE != 500, there must be something wrong
            // in the try block
            log.error(
                    "OauthController 500: can't add anything to page requests, b/c you're rate limited.",
                    e);
        }

        return toReturn;
    }

}
