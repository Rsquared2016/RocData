package in.fount.controller;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import twitter4j.RateLimitStatusEvent;
import twitter4j.RateLimitStatusListener;

public class LoggingRateLimitHandler implements
        RateLimitStatusListener {

    private static Logger log = LoggerFactory
            .getLogger(LoggingRateLimitHandler.class);

    public void onRateLimitStatus(RateLimitStatusEvent e) {
        log.warn("{}: {}", e.getRateLimitStatus(),
                e.isAccountRateLimitStatus());
    }

    public void onRateLimitReached(RateLimitStatusEvent e) {
        log.warn("Rate limit has been reached!");
        log.warn("{}: {}", e.getRateLimitStatus(),
                e.isAccountRateLimitStatus());
    }
}