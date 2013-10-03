package in.fount.controller;

import in.fount.model.mobile.ClassifyRequest;
import in.fount.model.mobile.Feedback;
import in.fount.model.mobile.GeoRequest;
import in.fount.model.mobile.SelfReport;
import in.fount.service.mobile.TweetMRepository;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseBody;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.servlet.ModelAndView;

@Controller
public class MobileController {

    private static final String TITLE = "GermTracker";

    @Autowired
    private TweetMRepository tweetRepo;

    @RequestMapping(value = { "/sf" }, method = RequestMethod.GET)
    public ModelAndView AboutFountin() {
        ModelAndView view = new ModelAndView("frisco");
        view.addObject("title", TITLE);
        return view;
    }

    @RequestMapping(value = { "/m", "/mobile" }, method = RequestMethod.GET)
    public ModelAndView retrieveMobile() {
        ModelAndView view = new ModelAndView("mobile");
        view.addObject("title", TITLE);
        return view;
    }

    @RequestMapping(value = { "/m/data", "/mobile/data" }, method = RequestMethod.GET)
    public @ResponseBody
    GeoRequest getTweets(
            @RequestParam("left") double left,
            @RequestParam("bottom") double bottom,
            @RequestParam("right") double right,
            @RequestParam("top") double top,
            @RequestParam(value = "health", required = false) Double health,
            @RequestParam(value = "user_lat", required = false) Double user_lat,
            @RequestParam(value = "user_lon", required = false) Double user_lon) {

        return tweetRepo.getTweets(left, bottom, right, top, health, user_lat,
                user_lon);
    }

    @RequestMapping(value = { "/m/data", "/mobile/data" }, method = RequestMethod.POST, produces = "application/json")
    @ResponseStatus(HttpStatus.ACCEPTED)
    public @ResponseBody
    ClassifyRequest postTweets(@RequestBody ClassifyRequest tweets) {
        return tweetRepo.postTweets(tweets);
    }

    @RequestMapping(value = { "/m/data/{id}", "/mobile/data/{id}" }, method = RequestMethod.POST, produces = "text/plain")
    @ResponseStatus(HttpStatus.ACCEPTED)
    public @ResponseBody
    String postFeedback(@PathVariable String id,
            @RequestParam(value = "lat") double lat,
            @RequestParam(value = "lng") double lng,
            @RequestBody Feedback feedback) {
        return tweetRepo.postFeedback(feedback, id, lat, lng);
    }

    @RequestMapping(value = { "/m/report", "/mobile/report" }, method = RequestMethod.POST, produces = "text/plain")
    @ResponseStatus(HttpStatus.ACCEPTED)
    public @ResponseBody
    String postSelfReport(@RequestBody SelfReport selfReport) {
        return tweetRepo.postSelfReport(selfReport);
    }

}
